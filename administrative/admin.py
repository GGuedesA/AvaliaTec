from django.contrib import admin
from .models import Block, Coordination, Room, Banca, AgendamentoSala

class BlockAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class CoordinationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'block')
    search_fields = ('name', 'block__name')
    list_filter = ('block',)
    ordering = ('name',)

class BancaAdmin(admin.ModelAdmin):
    list_display = ('tema', 'tipo', 'data', 'horario_inicio', 'horario_fim', 'status', 'sala')
    search_fields = ('tema', 'sala__name', 'alunos_nomes')
    list_filter = ('tipo', 'status', 'data', 'sala')
    ordering = ('-data', 'horario_inicio')

class AgendamentoSalaAdmin(admin.ModelAdmin):
    list_display = ('professor', 'sala', 'materia', 'data', 'horario_inicio', 'horario_fim', 'status')
    search_fields = ('professor__name', 'sala__name', 'materia')
    list_filter = ('status', 'data', 'sala')
    ordering = ('-data', 'horario_inicio')

admin.site.register(Block, BlockAdmin)
admin.site.register(Coordination, CoordinationAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Banca, BancaAdmin)
admin.site.register(AgendamentoSala, AgendamentoSalaAdmin)