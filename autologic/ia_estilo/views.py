import base64
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse


from .services import analizar_foto, recomendar_sobre_corte


@login_required(login_url='login')
def recomendador(request):
    resultado = None
    foto_preview = None

    # Recuperar análisis anterior de la sesión
    resultado_sesion = request.session.get("analisis_ia")

    if resultado_sesion:
        resultado = resultado_sesion

    if request.method == 'POST':
        foto = request.FILES.get('foto')
        acepto = request.POST.get('acepto_privacidad') == 'on'

        if not acepto:
            messages.error(
                request,
                'Debes aceptar el aviso de procesamiento de la fotografía.'
            )

        elif not foto:
            messages.error(
                request,
                'Selecciona una fotografía antes de analizar.'
            )

        else:
            try:
                contenido = foto.read()

                foto_preview = (
                    f"data:{foto.content_type};base64,"
                    f"{base64.b64encode(contenido).decode('utf-8')}"
                )

                from io import BytesIO
                foto.seek(0)

                # ==========================================
                # ANALIZAR CON IA
                # ==========================================
                resultado = analizar_foto(foto)

                # ==========================================
                # GUARDAR EL RESULTADO EN LA SESIÓN
                # ==========================================
                request.session["analisis_ia"] = resultado
                request.session.modified = True

            except (ValueError, RuntimeError) as exc:
                messages.error(request, str(exc))

            except Exception:
                messages.error(
                    request,
                    'Ocurrió un error inesperado al analizar la fotografía.'
                )

    return render(
        request,
        'ia_estilo/recomendador.html',
        {
            'resultado': resultado,
            'foto_preview': foto_preview,
        }
    )
@login_required(login_url='login')
def chat_corte(request):

    if request.method != 'POST':
        return JsonResponse(
            {
                'ok': False,
                'error': 'Método no permitido.'
            },
            status=405
        )

    try:
        payload = json.loads(
            request.body or '{}'
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {
                'ok': False,
                'error': 'Solicitud inválida.'
            },
            status=400
        )

    pregunta = str(
        payload.get('pregunta', '')
    ).strip()

    # Recuperamos el análisis que hizo AutoAI
    resultado = request.session.get(
        'analisis_ia'
    )

    if not resultado:
        return JsonResponse(
            {
                'ok': False,
                'error': 'Primero realiza el análisis con AutoAI.'
            },
            status=400
        )

    try:

        respuesta = recomendar_sobre_corte(
            pregunta,
            resultado
        )

        return JsonResponse(
            {
                'ok': True,
                **respuesta
            }
        )

    except ValueError as exc:

        return JsonResponse(
            {
                'ok': False,
                'error': str(exc)
            },
            status=400
        )

    except RuntimeError as exc:

        return JsonResponse(
            {
                'ok': False,
                'error': str(exc)
            },
            status=502
        )

    except Exception:

        return JsonResponse(
            {
                'ok': False,
                'error': (
                    'Ocurrió un error al consultar AutoAI.'
                )
            },
            status=500
        )