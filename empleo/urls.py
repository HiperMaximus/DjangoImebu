from django.urls import path
from . import views

app_name='empleo'

urlpatterns = [
    path('empleoDashboard/', views.empleoDashboard, name="empleoDashboard"),
]