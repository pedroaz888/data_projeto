from django.shortcuts import render
from .models import Usuario
from django.shortcuts import redirect
from .models import Usuario
from datetime import datetime
#import locale
#locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

from django.shortcuts import render

def home(request):
    return render(request, 'usuarios/home.html')


def usuarios(request):
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        data_da_festa = request.POST.get('data_da_festa')
        endereco = request.POST.get('endereco')

        novo_usuario = Usuario()
        novo_usuario.nome_cliente = nome_cliente  
        novo_usuario.data_da_festa = datetime.strptime(data_da_festa, '%Y-%m-%d')
        novo_usuario.endereco = endereco

        novo_usuario.save()

        return redirect('usuarios')
    else:
        #locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        usuarios = Usuario.objects.all()
        for usuario in usuarios:
            if usuario.data_da_festa is not None:
                usuario.data_da_festa = usuario.data_da_festa.strftime('%d de %B de %Y')
        return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})
    

def buscar_nomes(request):
    if request.method == 'GET':
        query = request.GET.get('nome_busca')
        usuarios = Usuario.objects.filter(nome_cliente__icontains=query)
        for usuario in usuarios:
            if usuario.data_da_festa is not None:
                usuario.data_da_festa = usuario.data_da_festa.strftime('%d de %B de %Y')
        return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})
    

def buscar_datas(request):
    if request.method == 'GET':
        data_inicial = request.GET.get('data_inicial')
        data_final = request.GET.get('data_final')
        if data_inicial and data_final:
            try:
                data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
                data_final = datetime.strptime(data_final, '%Y-%m-%d')
            except ValueError:
                mensagem = 'Datas inválidas. Por favor, informe datas no formato AAAA-MM-DD.'
                return render(request, 'usuarios/usuarios.html', {'mensagem': mensagem})
            usuarios = Usuario.objects.filter(data_da_festa__range=[data_inicial, data_final])
            for usuario in usuarios:
                if usuario.data_da_festa is not None:
                    usuario.data_da_festa = usuario.data_da_festa.strftime('%d de %B de %Y')
            return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})
        else:
            mensagem = 'Por favor, informe uma data inicial e uma data final para a busca.'
            return render(request, 'usuarios/usuarios.html', {'mensagem': mensagem})


def editar_usuario(request, id):
    usuario = Usuario.objects.get(id_usuario=id)
    
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        data_da_festa = request.POST.get('data_da_festa')
        endereco = request.POST.get('endereco')

        usuario.nome_cliente = nome_cliente  
        usuario.data_da_festa = datetime.strptime(data_da_festa, '%Y-%m-%d')
        usuario.endereco = endereco

        usuario.save()

        return redirect('usuarios')
    else:
        return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})





def excluir_usuario(request, id):
    usuario = Usuario.objects.get(id_usuario=id)
    usuario.delete()
  
    return redirect('usuarios')