from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, FileResponse
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TipoMascotaForm, PostMascotaForm


# Create your views here.
def ingreso(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Bienvenido, ingresaste correctamente")
            return HttpResponseRedirect(reverse('app1:home'))
        else:
            messages.error(request,"Usuario o contraseña incorrectos")
            return HttpResponseRedirect(reverse('app1:ingreso'))
    return render(request,'ingresoUsuario.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request,"El usuario y la contraseña son obligatorios")
            return HttpResponseRedirect(reverse('app1:registro'))
        
        if User.objects.filter(username=username).exists():
            messages.error(request,"Este nombre de usuario ya existe")
            return HttpResponseRedirect(reverse('app1:registro'))

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request,"Usuario creado correctamente")
        return HttpResponseRedirect(reverse('app1:ingreso'))
    return render(request,'registroUsuario.html')


@login_required(login_url='/')
def home(request):
    tipos = TipoMascota.objects.all()
    mascotas = Mascota.objects.all()
    return render(request,'home.html',{
        'tipos':tipos,
        'mascotas':mascotas
    })

@login_required(login_url='/')
def crearTipo(request):
    if request.method == 'POST':
        form = TipoMascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app1:home'))
    else:
        form = TipoMascotaForm()
    tipos = TipoMascota.objects.all()
    return render(request,'crearTipo.html',{
        'tipos':tipos,
        'form':form
    })

"""   
def crearTipo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        TipoMascota.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )
        return HttpResponseRedirect(reverse('app1:home'))
    tipos = TipoMascota.objects.all()
    return render(request,'crearTipo.html',{
        'tipos':tipos
    })
"""

@login_required(login_url='/')
def crearMascota(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        descripcion = request.POST.get('descripcion')
        idTipo = request.POST.get('tipo')
        foto = request.FILES.get('foto')
        tipo = TipoMascota.objects.get(id=idTipo)
        Mascota.objects.create(
            nombre=nombre,
            edad=edad,
            descripcion=descripcion,
            foto=foto,
            tipo=tipo,
            estado='Disponible'
        )
        return HttpResponseRedirect(reverse('app1:home'))
    tipos = TipoMascota.objects.all()
    return render(request,'crearMascota.html',{
        'tipos':tipos
    })

@login_required(login_url='/')
def mascotasxtipo(request,idTipo):
    tipos = TipoMascota.objects.all()
    tipo = TipoMascota.objects.get(id=idTipo)
    mascotas = Mascota.objects.filter(tipo=tipo)
    return render(request,'home.html',{
        'tipos':tipos,
        'mascotas':mascotas,
        'tipo_seleccionado':tipo
    })

@login_required(login_url='/')
def detalleMascota(request,idMascota):
    mascota = Mascota.objects.get(id=idMascota)
    tipos = TipoMascota.objects.all()
    adopcion = None

    if mascota.estado == 'Adoptado':
        try:
            adopcion = Adopcion.objects.get(mascota=mascota)
        except Adopcion.DoesNotExist:
            adopcion = None
    
    if request.method == 'POST' and mascota.estado == 'Disponible':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')

        persona = Persona.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono
        )

        Adopcion.objects.create(
            mascota=mascota,
            persona=persona,
            fecha_adopcion=datetime.now().strftime("%d/%m/%Y %H:%M")
        )

        mascota.estado = 'Adoptado'
        mascota.save()
        return HttpResponseRedirect(reverse('app1:detalleMascota', args=[mascota.id]))

    return render(request,'detalleMascota.html',{
        "tipos":tipos,
        "adopcion": adopcion,
        "mascota":mascota,
    })

@login_required(login_url='/')
def listaAdoptantes(request):
    tipos = TipoMascota.objects.all()
    adopciones = Adopcion.objects.all()
    return render(request,'listaAdoptantes.html',{
        'tipos':tipos,
        'adopciones':adopciones
    })

@login_required(login_url='/')
def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('app1:ingreso'))

@login_required(login_url='/')
def posts_mascota(request, mascota_id):
    # Vista para ver y registrar posts (galería) de una mascota
    tipos = TipoMascota.objects.all()
    mascota = get_object_or_404(Mascota, id=mascota_id)

    posts = PostMascota.objects.filter(mascota=mascota).order_by('-fecha', '-id')

    if request.method == 'POST':
        form = PostMascotaForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.mascota = mascota
            post.save()
            return HttpResponseRedirect(reverse('app1:posts_mascota', args=[mascota.id]))
    else:
        form = PostMascotaForm()

    return render(request, 'posts_mascota.html', {
        'tipos': tipos,
        'mascota': mascota,
        'form': form,
        'posts': posts
    })
