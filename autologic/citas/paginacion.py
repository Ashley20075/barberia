"""
Paginación reutilizable para listas largas de citas (historial del
cliente, del barbero y del admin). Antes cada panel mostraba TODO el
historial de una sola vez en una tabla que podía crecer sin límite
(como en la captura: decenas de filas sin forma de navegar). Esta
función centraliza la lógica para que los 3 paneles se comporten igual.
"""

from django.core.paginator import Paginator


def paginar(queryset, request, parametro="pagina", por_pagina=10):
    """
    Devuelve un objeto Page de Django listo para iterar en el template
    (misma interfaz que un queryset) y con los controles de "anterior/
    siguiente/números de página" ya calculados.
    """
    paginador = Paginator(queryset, por_pagina)
    numero_pagina = request.GET.get(parametro, 1)
    return paginador.get_page(numero_pagina)
