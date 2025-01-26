from django.db import models
from django.contrib.auth.models import User

#Modelo de Ubicacion
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)


    def __str__(self):
        return self.nombre

#Modelo de Evento
class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    imagen = models.ImageField(upload_to="events/", blank=True, null=True)
    capacidad = models.PositiveIntegerField(default=0)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="eventos", default=1)

    def __str__(self):
        return self.nombre

#Modelo del expositor
class Expositor(models.Model):
    nombre = models.CharField(max_length=255)
    biografia = models.TextField()
    imagen = models.ImageField(upload_to="repositories/", blank=True, null=True)

    def __str__(self):
        return self.nombre



#Modelo Ticket
class Ticket(models.Model):
    # Relación con el evento al que pertenece el ticket
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE)

    # Relación con el usuario (asistente) que adquirió el ticket
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # Código único para identificar el ticket
    codigo_qr = models.CharField(max_length=100, unique=True)

    # Estado del ticket: pendiente, confirmado o usado
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('confirmado', 'Confirmado'), ('usado', 'Usado')],
        default='pendiente'
    )


    # Campo para almacenar la imagen del código QR (opcional)
    qr_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.evento.nombre} ({self.usuario.username})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLES = [
        ('ORGANIZER', 'Organizador'),
        ('ASSISTANT', 'Asistente'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='ASSISTANT')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

