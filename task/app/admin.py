#from django.contrib import admin

#from app.models import Task

# Register your models here.
#admin.site.register(Task)
from django.contrib import admin
from .models import Evento, Ubicacion, Expositor, Ticket
admin.site.register(Evento)
admin.site.register(Ubicacion)
admin.site.register(Expositor)