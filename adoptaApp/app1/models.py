from django.db import models

# Create your models here.
class TipoMascota(models.Model):
    nombre = models.CharField(max_length=64,null=True,blank=True)
    descripcion = models.TextField(max_length=256,null=True,blank=True)

    def __str__(self):
        return self.nombre
    
class Mascota(models.Model):
    nombre = models.CharField(max_length=128,null=True,blank=True)
    edad = models.IntegerField()
    descripcion = models.TextField(max_length=512,null=True,blank=True)
    foto = models.ImageField(upload_to='mascotas/')
    tipo = models.ForeignKey(TipoMascota, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"
    
class Persona(models.Model):
    nombre = models.CharField(max_length=128,null=True,blank=True)
    email = models.CharField(max_length=128,null=True,blank=True)
    telefono = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.telefono}"
    
class Adopcion(models.Model):
    mascota = models.OneToOneField(Mascota, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha_adopcion = models.CharField(max_length=20,null=True,blank=True)

class PostMascota(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha = models.DateField()
    foto = models.ImageField(upload_to='posts_mascotas/')

    def __str__(self):
        return f"{self.mascota.nombre} - {self.titulo}"

