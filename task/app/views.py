from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Evento, Ticket, Profile
from django.shortcuts import render
from .forms import EventoForm
import random
import string

def home(request):
    return render(request, 'home.html')


def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not hasattr(request.user, 'profile') or request.user.profile.role not in allowed_roles:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'lista_eventos'))
        messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'tasks/login.html')


def register_user(request):
    if request.method == 'POST':
        data = request.POST
        if data['password'] != data['confirm_password']:
            messages.error(request, 'Las contraseñas no coinciden')
        elif User.objects.filter(username=data['username']).exists():
            messages.error(request, 'El nombre de usuario ya existe')
        elif User.objects.filter(email=data['email']).exists():
            messages.error(request, 'El correo ya está registrado')
        elif data.get('role') not in ['ADMIN', 'ORGANIZER', 'ASSISTANT']:
            messages.error(request, 'Selecciona un rol válido')
        else:
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            Profile.objects.create(user=user, role=data['role'])
            messages.success(request, 'Usuario creado exitosamente')
            login(request, user)
            return redirect('home')
    return render(request, 'tasks/register.html')


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')


@login_required
@role_required(['ADMIN', 'ORGANIZER'])
def crear_evento(request):
    form = EventoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        evento = form.save(commit=False)
        evento.creador = request.user
        evento.save()
        messages.success(request, 'Evento creado exitosamente.')
        return redirect('lista_eventos')
    return render(request, 'tasks/crear_evento.html', {'form': form})


@login_required
def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'tasks/lista_eventos.html', {'eventos': eventos})


@login_required
@role_required(['ASSISTANT'])
def comprar_boleto(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if evento.capacidad <= 0:
        return render(request, '', {'evento': evento})
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad'))
        if cantidad > evento.capacidad:
            messages.error(request, 'No hay suficientes lugares disponibles.')
        else:
            evento.capacidad -= cantidad
            evento.save()
            for _ in range(cantidad):
                codigo_qr = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                Ticket.objects.create(evento=evento, usuario=request.user, codigo_qr=codigo_qr, estado='pendiente')
            messages.success(request, 'Boletos comprados exitosamente.')
            return redirect('historial_compras')
    return render(request, 'tasks/comprar_boleto.html', {'evento': evento})


@login_required
def historial_compras(request):
    tickets = Ticket.objects.filter(usuario=request.user)
    return render(request, 'tasks/historial_compras.html', {'tickets': tickets})


@login_required
@role_required(['ADMIN', 'ORGANIZER'])
def gestionar_eventos(request):
    eventos = Evento.objects.filter(creador=request.user)
    return render(request, 'tasks/gestion_eventos.html', {'eventos': eventos})


@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, creador=request.user)
    form = EventoForm(request.POST or None, request.FILES or None, instance=evento)
    if form.is_valid():
        form.save()
        messages.success(request, 'Evento actualizado correctamente.')
        return redirect('gestionar_eventos')
    return render(request, 'tasks/editar_evento.html', {'form': form, 'evento': evento})


@login_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, creador=request.user)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado correctamente.')
        return redirect('gestionar_eventos')
    return render(request, 'tasks/eliminar_evento.html', {'evento': evento})


@login_required
def cambiar_estado_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    nuevo_estado = request.POST.get('estado')
    if nuevo_estado in ['Válido', 'Pendiente', 'Cancelado']:
        ticket.estado = nuevo_estado
        ticket.save()
        messages.success(request, f"Estado del ticket actualizado a {nuevo_estado}.")
    else:
        messages.error(request, "Estado inválido.")
    return redirect('gestion_tickets')

@login_required
@role_required(['ORGANIZER'])
def check_in_ticket(request, ticket_id):
    # Verificar si la solicitud es POST
    if request.method == "POST":
        # Buscar el ticket por ID
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if ticket.estado != "Válido":
            # Cambiar el estado del ticket
            ticket.estado = "Válido"
            ticket.save()
            messages.success(request, "Check-in realizado con éxito.")
        else:
            messages.warning(request, "Este ticket ya está marcado como válido.")
    return redirect("tasks/check_in")

@login_required
def agenda_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'tasks/agenda_eventos.html', {'eventos': eventos})


@login_required
@role_required(['ORGANIZER'])
def gestionar_tickets(request):
    if request.method == "POST":
        codigo_qr = request.POST.get("codigo_qr")
        # Lógica para verificar el ticket
        ticket = Ticket.objects.filter(codigo_qr=codigo_qr).first()
        if ticket:
            ticket.estado = "Válido"
            ticket.save()
            messages.success(request, "Check-in realizado con éxito.")
        else:
            messages.error(request, "Código QR no válido.")
    tickets = Ticket.objects.all()
    return render(request, "tasks/gestion_tickets.html", {"tickets": tickets})
