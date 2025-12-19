from django.urls import path, include
from . import views

app_name = 'app1'

urlpatterns = [
    path('',views.ingreso,name='ingreso'),
    path('registro',views.registro,name='registro'),
    path('home',views.home,name='home'),
    path('crearTipo',views.crearTipo,name='crearTipo'),
    path('crearMascota',views.crearMascota,name='crearMascota'),
    path('listaAdoptantes',views.listaAdoptantes,name='listaAdoptantes'),
    path('mascotasxtipo/<int:idTipo>',views.mascotasxtipo,name='mascotasxtipo'),
    path('detalleMascota/<int:idMascota>',views.detalleMascota,name='detalleMascota'),
    path('mascota/<int:mascota_id>/posts', views.posts_mascota, name='posts_mascota'),
    path('cerrarSesion',views.cerrarSesion,name='cerrarSesion')
    

]