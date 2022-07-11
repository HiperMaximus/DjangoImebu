from django.urls import path
from . import views

app_name='gateway'

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register-persona/', views.registerPagePersona, name="registerPersona"),
    path('register-empresa/', views.registerPageEmpresa, name="registerEmpresa"),

    path('', views.home, name="home"),
    path('dashboard/', views.mainDashboard, name="mainDashboard"),
]
