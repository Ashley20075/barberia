from django.urls import path
from . import views


app_name = 'ia_estilo'


urlpatterns = [
    path(
        '',
        views.recomendador,
        name='recomendador'
    ),
]