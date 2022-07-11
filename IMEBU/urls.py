"""IMEBU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.static import serve

@login_required(login_url='gateway:login')
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('gateway.urls')),
    path('observatorio/',include('observatorio.urls')),
    path('empleoJoven/',include('empleo_joven.urls')),
    path('empleo/',include('empleo.urls')),
    path('banca/',include('banca_ciudadana.urls')),

    re_path(r'^%s%s(?P<path>.*)$' % (settings.MEDIA_URL[1:],'protected'), protected_serve, {'document_root': str(settings.MEDIA_ROOT)+'\protected'})
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)