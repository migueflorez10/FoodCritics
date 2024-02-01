"""FoodCritics URL Configuration

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
from django.contrib import admin
from django.urls import path
from application import views as applicationViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', applicationViews.home, name='home'),
    path('restaurante/', applicationViews.enviarRestaurante),
    path('mapa/',applicationViews.mapa),
    path('tus-puntos/', applicationViews.puntos),
    path('menu/',applicationViews.menu),
    path('menuMayor/',applicationViews.menuMayor),
    path('menuMenor/',applicationViews.menuMenor),
    path('reviewMenu/', applicationViews.reviewMenu),
    path('registrarse/', applicationViews.Registro),
    path('ingreso/', applicationViews.Ingreso),
    path('home/', applicationViews.HomeIniciado, name='hom'),
    path('index/', applicationViews.logout_request, name='cerrar_sesion'),
    path('salto/', applicationViews.Salto),
    path('salto2/', applicationViews.Salto2),
    path('restauranteIniciado/', applicationViews.restauranteIniciado),
    path('mapaIngresado/', applicationViews.mapaIngresado),
    path('destacados/', applicationViews.destacados, name="destacados"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
