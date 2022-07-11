from django.urls import path
from . import views

app_name='empleoJoven'

urlpatterns = [
    path('Dashboard/', views.empleoJovenDashboard, name="empleoJovenDashboard"),
    path('RegistroEmpresa/', views.empleoJovenRegistroEmpresa, name="empleoJovenRegistroEmpresa"),

    path('AddGeneralDocument/<str:nombre_documento>', views.empleoJovenAddDocumentGeneral, name="empleoJovenAddDocumentGeneral"),
    path('AddJovenDocument/<str:nombre_documento>', views.empleoJovenAddDocumentJoven, name="empleoJovenAddDocumentJoven"),

    path('UpdateDocumentGeneral/<int:pk>/<str:nombre_documento>', views.empleoJovenUpdateDocumentGeneral, name="empleoJovenUpdateDocumentGeneral"),
    path('UpdateDocumentJoven/<int:pk>/<str:nombre_documento>', views.empleoJovenUpdateDocumentJoven, name="empleoJovenUpdateDocumentJoven"),

    path('DeleteDocument/<int:pk>', views.empleoJovenDeleteDocumentJoven, name="empleoJovenDeleteDocumentJoven"),

    path('RegistroEmpleados/', views.empleoJovenRegistroEmpleados, name="empleoJovenRegistroEmpleados"),
    path('AddEmpleado/', views.empleoJovenAddEmpleado, name="empleoJovenAddEmpleado"),
    path('DeleteEmpleado/<int:pk>', views.empleoJovenDeleteEmpleado, name="empleoJovenDeleteEmpleado"),
    path('UpdateEmpleado/<int:pk>', views.empleoJovenUpdateEmpleado, name="empleoJovenUpdateEmpleado"),
]
