"""
URL configuration for eduplanner_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from eduplanner import views
from Calendar.views import calendar_view
from api import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.pag_principal, name='pag_principal'),
    path('api/calendario/', views.CalendarioAPIView.as_view(), name='calendario'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('calendar/', calendar_view, name='calendar' ),
    path('api/', include('api.urls')),
    path('agregar-evento/', views.agregar_evento, name='agregar_evento'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('editar-evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eliminar-evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
]

# Solo para desarrollo. Esto permite que el servidor de Django sirva archivos estáticos (como imágenes).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
