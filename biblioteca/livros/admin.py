from django.contrib import admin
from .models import Autor, Livros, Cliente
from .models import Emprestimo

admin.site.register(Emprestimo)
admin.site.register(Autor)
admin.site.register(Livros)
admin.site.register(Cliente)