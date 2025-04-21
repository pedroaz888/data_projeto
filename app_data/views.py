from django.shortcuts import render
from .models import Usuario
from django.shortcuts import redirect
from .models import Usuario
from datetime import datetime
from django.http import JsonResponse
from fpdf import FPDF
from django.http import FileResponse
from io import BytesIO
from math import sqrt

#import locale
#locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

from django.shortcuts import render

def home(request):
    return render(request, 'usuarios/home.html')
    

def usuarios(request, importantes=None):
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        data_da_festa_str = request.POST.get('data_da_festa')
        endereco = request.POST.get('endereco')
        datas_importantes = request.POST.get('datas_importantes') == 'True'

        data_da_festa = datetime.strptime(data_da_festa_str, '%Y-%m-%d').date()

        novo_usuario = Usuario(nome_cliente=nome_cliente,
                               data_da_festa=data_da_festa,
                               endereco=endereco,
                               datas_importantes=datas_importantes)
        novo_usuario.save()

        return redirect('usuarios')
    else:
        if importantes is not None:
            usuarios = Usuario.objects.filter(datas_importantes=True)
        else:
            usuarios = Usuario.objects.all()

        for usuario in usuarios:
            if usuario.data_da_festa is not None:
                usuario.data_da_festa = usuario.data_da_festa.strftime('%d/%m/%Y')

        return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})


def buscar_nomes(request):
    if request.method == 'GET':
        query = request.GET.get('nome_busca')
        usuarios = Usuario.objects.filter(nome_cliente__icontains=query)
        for usuario in usuarios:
            if usuario.data_da_festa is not None:
                usuario.data_da_festa = usuario.data_da_festa.strftime('%d/%m/%Y')
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
                    usuario.data_da_festa = usuario.data_da_festa.strftime('%d/%m/%Y')
            return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})
        else:
            mensagem = 'Por favor, informe uma data inicial e uma data final para a busca.'
            return render(request, 'usuarios/usuarios.html', {'mensagem': mensagem})



def editar_usuario(request, id):
    usuario = Usuario.objects.get(id_usuario=id)
    
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        data_da_festa_str = request.POST.get('data_da_festa')
        endereco = request.POST.get('endereco')
        datas_importantes = request.POST.get('datas_importantes') == 'on'

        data_da_festa = datetime.strptime(data_da_festa_str, '%Y-%m-%d').strftime('%Y-%m-%d')

        usuario.nome_cliente = nome_cliente  
        usuario.data_da_festa = data_da_festa
        usuario.endereco = endereco
        usuario.datas_importantes = datas_importantes

        usuario.save()

        return redirect('usuarios')
    else:
       
        return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})


def datas_importantes(request):
    usuarios = Usuario.objects.filter(datas_importantes=True)
    for usuario in usuarios:
        if usuario.data_da_festa is not None:
            usuario.data_da_festa = usuario.data_da_festa.strftime('%d/%m/%Y')
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})


def excluir_usuario(request, id):
    usuario = Usuario.objects.get(id_usuario=id)
    usuario.delete()
  
    return redirect('usuarios')


def gerar_pdf(request):
    usuarios = Usuario.objects.filter(datas_importantes=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 8)
    pdf.set_fill_color(240, 240, 240)

    # Cabeçalhos
    headers = ['Nome', 'Data', 'Endereço']

    # Dados da tabela
    data = []
    for usuario in usuarios:
        data.append([usuario.nome_cliente, usuario.data_da_festa.strftime('%d/%m/%Y'), usuario.endereco])

    # Criar tabela
    pdf.set_font("Arial", "B", 10)
    cell_width = pdf.w / 3
    cell_height = 10
    pdf.cell(cell_width, cell_height, headers[0], 1, 0, 'C', 1)
    pdf.cell(cell_width, cell_height, headers[1], 1, 0, 'C', 1)
    pdf.cell(cell_width, cell_height, headers[2], 1, 1, 'C', 1)

    pdf.set_font("Arial", "", 10)
    for row in data:
        for item in row:
            pdf.cell(cell_width, cell_height, str(item), 1, 0, 'L')
        pdf.ln(cell_height)

    pdf_content = pdf.output(dest='S').encode('latin1')
    pdf_bytes = BytesIO(pdf_content)

    response = FileResponse(pdf_bytes, as_attachment=True, filename='usuarios.pdf')
    return response



