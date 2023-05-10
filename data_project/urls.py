
from django.contrib import admin
from django.urls import path
from app_data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('excluir_usuario/<int:id>/', views.excluir_usuario, name='excluir_usuario'),
    path('buscar_nomes/', views.buscar_nomes, name='buscar_nomes'),
    path('buscar_datas/', views.buscar_datas, name='buscar_datas'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('datas_importantes', views.datas_importantes, name='datas_importantes'),
    path('gerar_pdf', views.gerar_pdf, name='gerar_pdf'),

  
]
