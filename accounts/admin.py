from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'name', 'email', 'role', 'is_active', 'date_joined')
    search_fields = ('cpf', 'name', 'email')
    list_filter = ('role', 'is_active')
    ordering = ('-date_joined',)

admin.site.register(Usuario, UsuarioAdmin)