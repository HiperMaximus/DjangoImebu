from django.urls import path
from . import views

app_name='observatorio'

urlpatterns = [
    path('observatorioDashboard/', views.observatorioDashboard, name="observatorioDashboard"),
    path('IndicadorMercadoLaboral/', views.indicadorMercadoLaboral, name="indicadorMercLaboral"),
    path('IndicadorMacroeconomico/', views.indicadorMacroeconomico, name="indicadorMacroeconomico"),
    path('IndicadorPulsoSocial/', views.indicadorPulsoSocial, name="indicadorPulsoSocial"),
    path('IndicadorEmpresarial/', views.indicadorEmpresarial, name="indicadorEmpresarial"),
]