from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # Home y autenticación
    path('admin/', admin.site.urls, name='admin'),
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    # Eventos
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    path('eventos/gestion/', views.gestionar_eventos, name='gestionar_eventos'),
    path('eventos/editar/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('eventos/agenda_evento/', views.agenda_eventos, name='agenda_eventos'),

    # Tickets
    path('eventos/<int:evento_id>/comprar/', views.comprar_boleto, name='comprar_boleto'),
    path('tickets/historial/', views.historial_compras, name='historial_compras'),
    path('tickets/gestion/', views.gestionar_tickets, name='gestion_tickets'),
    path('tickets/editar_estado/<int:ticket_id>/', views.cambiar_estado_ticket, name='cambiar_estado_ticket'),
    path('tickets/check-in/<int:ticket_id>/', views.check_in_ticket, name='check_in_ticket'),
]

# Rutas para servir archivos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
