from dataclasses import field, fields
from django import forms
from .models import cat_P, ges_P, review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator

class registro_usuario (forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

class categoria_P (forms.ModelForm):
    name = forms.CharField (required=True, label= 'Nombre de la categoria:')
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 35}))

    class Meta:
        model = cat_P
        fields = ['name', 'descripcion']

class gestion_P (forms.ModelForm):
    name = forms.CharField (required=True, label='Ingrese el nombre del producto')
    descripcion = forms.Textarea()
    precio = forms.DecimalField(required=True, label='Ingrese el precio del producto')
    img = forms.ImageField(required=False, label="Seleccione una imagen")
    categoria = forms.ModelChoiceField(queryset=cat_P.objects.all(), 
                empty_label="Selecciona una categoría",  
                label="Categoría", required=True)
    
    class Meta:
        model = ges_P
        fields = ['name', 'descripcion', 'precio', 'img', 'categoria']

class review_Form (forms.ModelForm):
    class Meta:
        model = review
        fields = ['opinion', 'calificacion']