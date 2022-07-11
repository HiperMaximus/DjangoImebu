from django.urls import path
from . import views

app_name='bancaCiudadana'

urlpatterns = [
    path('postulacion-primerPaso/', views.bancaPostulacionFase1, name="bancaPostulacionFase1"),
    path('postulacion-segundoPaso/', views.bancaPostulacionFase2, name="bancaPostulacionFase2"),
]
