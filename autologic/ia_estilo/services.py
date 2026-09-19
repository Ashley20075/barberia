import base64
import json
import os
from io import BytesIO

import requests
from PIL import Image, ImageOps


MODEL = os.getenv('GEMINI_MODEL', 'gemini-3.5-flash-lite')

API_URL = (
    f'https://generativelanguage.googleapis.com/'
    f'v1beta/models/{MODEL}:generateContent'
)


PROMPT = '''
Eres el asistente de estilo de una barbería llamada AUTOLOGIC.

Analiza la fotografía únicamente usando características VISIBLES.

No intentes identificar a la persona, su identidad, edad, raza, etnia,
salud, diagnósticos, emociones ni otros atributos sensibles.

Tu objetivo es orientar al cliente sobre cortes de cabello que podría considerar.

No afirmes que un corte le quedará bien con certeza.
Presenta las opciones como recomendaciones orientativas y recuerda que
el barbero debe validar el resultado.

Ten en cuenta, cuando sea visible:

- forma/apariencia general del rostro;
- longitud actual del cabello;
- volumen visible;
- textura aparente del cabello;
- línea del cabello visible;
- estilo actual.

Devuelve SOLO JSON válido, sin markdown, con esta estructura exacta:

{
  "observaciones": ["...", "..."],
  "recomendaciones": [
    {
      "nombre": "Nombre del corte",
      "motivo": "Explicación breve basada en rasgos visibles y preferencias de estilo",
      "mantenimiento": "Bajo | Medio | Alto",
      "pedido_barbero": "Cómo podría pedirlo al barbero"
    }
  ],
  "aviso": "Una frase breve indicando que es una recomendación orientativa."
}

Incluye 3 recomendaciones diferentes.

Si la foto no muestra suficientemente bien el cabello o el rostro,
dilo en observaciones y evita inventar características.
'''


def _prepare_image(uploaded_file):
    allowed = {
        'image/jpeg',
        'image/png',
        'image/webp'
    }

    if uploaded_file.content_type not in allowed:
        raise ValueError(
            'Solo se aceptan imágenes JPG, PNG o WEBP.'
        )

    if uploaded_file.size > 5 * 1024 * 1024:
        raise ValueError(
            'La imagen no puede superar los 5 MB.'
        )

    uploaded_file.seek(0)

    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)

    image.thumbnail((1200, 1200))
    image = image.convert('RGB')

    output = BytesIO()

    image.save(
        output,
        format='JPEG',
        quality=85,
        optimize=True
    )

    return output.getvalue(), 'image/jpeg'


def _extract_json(text):
    text = (text or '').strip()

    if text.startswith('```'):
        lines = text.splitlines()

        if len(lines) > 2:
            lines = lines[1:-1]

        text = '\n'.join(lines)

        if text.startswith('json\n'):
            text = text.replace('json\n', '', 1)

        text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        start = text.find('{')
        end = text.rfind('}')

        if start >= 0 and end > start:
            return json.loads(
                text[start:end + 1]
            )

        raise ValueError(
            'La IA devolvió una respuesta que no se pudo interpretar.'
        )


def analizar_foto(uploaded_file):

    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        raise RuntimeError(
            'Falta GEMINI_API_KEY en el archivo .env. '
            'Crea una clave gratuita en Google AI Studio.'
        )

    image_bytes, mime_type = _prepare_image(
        uploaded_file
    )

    image_b64 = base64.b64encode(
        image_bytes
    ).decode('utf-8')

    payload = {
        'contents': [
            {
                'parts': [
                    {
                        'text': PROMPT
                    },
                    {
                        'inline_data': {
                            'mime_type': mime_type,
                            'data': image_b64,
                        }
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.4,
            'maxOutputTokens': 1200,
            'responseMimeType': 'application/json',
        },
    }

    response = requests.post(
        API_URL,
        headers={
            'x-goog-api-key': api_key,
            'Content-Type': 'application/json',
        },
        json=payload,
        timeout=45,
    )

    if response.status_code != 200:

        try:
            detail = response.json().get(
                'error',
                {}
            ).get(
                'message',
                ''
            )

        except ValueError:
            detail = response.text[:300]

        raise RuntimeError(
            f'Google Gemini respondió con error '
            f'({response.status_code}): {detail}'
        )

    data = response.json()

    try:

        text = (
            data['candidates'][0]
            ['content']['parts'][0]
            ['text']
        )

    except (
        KeyError,
        IndexError,
        TypeError
    ):

        raise RuntimeError(
            'La IA no devolvió contenido utilizable. '
            'Inténtalo de nuevo.'
        )

    result = _extract_json(text)

    result.setdefault(
        'observaciones',
        []
    )

    result.setdefault(
        'recomendaciones',
        []
    )

    result.setdefault(
        'aviso',
        'La recomendación es orientativa; '
        'el barbero debe validar el corte.'
    )

    return result