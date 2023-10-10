from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import categoria_P, gestion_P, review_Form, registro_usuario
from django.contrib.auth.decorators import login_required
from .models import cat_P, ges_P, review, User



def register(request):
    if request.method == 'POST':
        form = registro_usuario(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if not User.objects.filter(username=username).exists():
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    return redirect('login')
                except IntegrityError:
                        form.add_error(None, "Ocurrió un error al registrar el usuario.")
            else:
                form.add_error('username', "El nombre de usuario ya está en uso.")
    else:
        form = registro_usuario()

    return render(request, 'register.html', {'form': form})

def menu(request):
    solicitud = ges_P.objects.all()
    catego2 = request.GET.get('categoria', '')
    catego = cat_P.objects.values('name').distinct()

    if catego2:
        solicitud = solicitud.filter(categoria__name=catego2)

    return render (request, 'menu.html', {'solicitud': solicitud, 'catego' : catego, 'catego2' : catego2})

def Categoria_P (request):
    categorias = cat_P.objects.all()
    
    if request.method == 'POST':
        form = categoria_P(request.POST)
        if form.is_valid():
            form.save()
            return redirect (reverse('Categoria_P'))
    else:
        form = categoria_P()
    
    return render (request, 'Categoria_P.html' , {'form': form, 'categorias' : categorias})

def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(cat_P, pk=categoria_id)

    if request.method == 'POST':
        form = categoria_P(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect(reverse('Categoria_P')) 
    else:
        form = categoria_P(instance=categoria)
 
    return render(request, 'editar_categoria.html', {'form': form, 'categoria': categoria})

def eliminar_registro(request, registro_id):
    registro = get_object_or_404(cat_P, pk=registro_id)
    registro.delete()
    return redirect('Categoria_P')

def Gestion_P(request, categoria=None):
    categoria = request.GET.get('categoria', '')

    categorias = cat_P.objects.values('name').distinct()

    productos = ges_P.objects.all()

    if categoria:
        productos = productos.filter(categoria__name=categoria)

    if request.method == 'POST':
        form = gestion_P(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestion_P'))
    else:
        form = gestion_P()
    
    return render(request, 'gestion_P.html', {'form': form, 'productos': productos, 
                'categorias': categorias, 'categoria_seleccionada': categoria})

def editar_producto(request, categoria_id):
    productos = get_object_or_404(ges_P, pk=categoria_id)

    if request.method == 'POST':
        form = gestion_P(request.POST, request.FILES, instance=productos)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestion_P')) 
    else:
        form = gestion_P(instance=productos)
 
    return render(request, 'productos_E.html', {'form': form, 'productos': productos})

def eliminar_producto(request, registro_id):
    registro = get_object_or_404(ges_P, pk=registro_id)
    registro.delete()
    return redirect('gestion_P')


def detalles_producto(request, categoria_id):
    producto = get_object_or_404(ges_P, pk=categoria_id)
    comentarios = review.objects.filter(nameP=producto)

    origen = request.GET.get('origen')

    if request.method == 'POST':
        form = gestion_P(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect(reverse('gestion_P')) 
    else:
        form = gestion_P(instance=producto)
 
    return render(request, 'detalle_productos.html', {'form': form, 'producto': producto, 'origen': origen,
                                                      'comentarios' : comentarios})

def reviewss(request):
    namePro = ges_P.objects.values('name').distinct()
    error = None
    prod_selec = None
    review_pro = None
    
    if request.method == 'POST':
        form = review_Form(request.POST)
        producto_nombre = request.POST.get('Productos')
 
        
        if producto_nombre:
            producto = ges_P.objects.get(name=producto_nombre)
            form.instance.nameP = producto
        
            if form.is_valid():
                form.save()
                review_pro = review.objects.filter(nameP=producto)
                prod_selec = producto_nombre
                return redirect('review')
        else:
            error = "Por Favor, Seleccione una de las opciones"
            
    else:
        form = review_Form()
    
    return render (request, 'review.html', {'form': form, 'namePro' : namePro, 
                            'prod_selec' : prod_selec, 'error' : error,
                            'review_pro' : review_pro,})

def mostrar_todos (request):
    productos = ges_P.objects.all()

    # Filtrar por categoría si se proporciona un parámetro en la URL
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria=categoria_id)

    # Configurar la paginación (8 productos por página)
    paginator = Paginator(productos, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Obtener todas las categorías (útiles para el filtro)
    categorias = cat_P.objects.all()

    return render(request, 'vertodos_P.html', {'page_obj': page_obj, 'categorias': categorias})