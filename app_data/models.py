from django.db import models

from django.db import models
from urllib.parse import urlencode
from datetime import datetime



    
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome_cliente = models.TextField(max_length=100, null=False, blank=False, default=None)
    data_da_festa = models.DateField()
    endereco = models.TextField(max_length=600, null=False, blank=False, default=None)
   
    def __str__(self):
        return self.nome_cliente
    
    @property
    def google_maps_url(self):
        base_url = 'https://www.google.com/maps/search/?api=1'
        params = {
            'query': self.endereco,
        }
        return f'{base_url}&{urlencode(params)}'
    

    
    def data_da_festa_formatted(self):
        return self.data_da_festa.strftime("%d/%m/%Y")
