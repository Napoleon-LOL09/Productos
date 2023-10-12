from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

main_app = 'main'

urlpatterns = [
    path ('', LoginView.as_view(template_name='base.html'), name='login'),
    path ('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'), 
    path ('register/' , views.register, name="register"),
    path ('menu/', views.menu, name='menu'),
    path ('Categoria_P/', views.Categoria_P, name="Categoria_P"),
    path ('editar_categoria/<int:categoria_id>/', views.editar_categoria, name="editar_categoria"),
    path ('eliminar_registro/<int:registro_id>/', views.eliminar_registro, name='eliminar_registro'),
    path ('gestion_P/', views.Gestion_P, name='gestion_P'),
    path ('productos_E/<int:categoria_id>/', views.editar_producto, name="productos_E"),
    path ('eliminar_producto/<int:registro_id>/', views.eliminar_producto, name='eliminar_producto'),
    path ('detalle_productos/<int:categoria_id>/', views.detalles_producto, name='detalle_productos'),
    path ('review/', views.reviewss, name='review'),
    path ('vertodos_P/', views.mostrar_todos, name='vertodos_P'),

	]