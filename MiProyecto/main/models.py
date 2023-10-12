from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

class cat_P (models.Model):
    class Meta:
        verbose_name_plural = 'Categorias'
        verbose_name = 'Categoria'
        db_table = 'cat_P'
    
    name = models.CharField(max_length=20, blank=False, null=False, unique=True)
    descripcion = models.TextField(max_length=100, blank=False, null=False, unique=True)
    
    def __str__(self):
        return self.name

class ges_P (models.Model):
    class Meta:
        verbose_name_plural = 'Productos'
        verbose_name = 'Producto'
        db_table = 'ges_P'
    
    name = models.CharField (max_length=20, blank=False, null=False, unique=True)
    descripcion = models.CharField(max_length=100, blank=False, null=False)
    precio = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10)
    img = models.ImageField(upload_to='productos/', blank=True)
    categoria = models.ForeignKey(cat_P, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class review (models.Model):
    class Meta:
        verbose_name_plural = 'Reviews'
        verbose_name = 'Review'
        db_table = 'review'

    nameP = models.ForeignKey(ges_P, on_delete=models.CASCADE)
    opinion = models.TextField (blank=False, null=False)
    calificacion = models.DecimalField(max_digits=3, decimal_places=1,
        choices=[
            (1, '1 estrella'), (1.5, '1.5 estrellas'), (2, '2 estrellas'),
            (2.5, '2.5 estrellas'), (3, '3 estrellas'), (3.5, '3.5 estrellas'),
            (4, '4 estrellas'), (4.5, '4.5 estrellas'), (5, '5 estrellas')
        ],
        default=1.0, 
    )

