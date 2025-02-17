from django.urls import path
from .views import BancaList, BancaDetail, AgendamentoSalaList, AgendamentoSalaDetail

app_name = "administrative"
urlpatterns = [
    # URLs para Banca de Defesa
    path("bancas_list/", BancaList.as_view(), name="banca_list"),
    path("bancas_list/<int:pk>/", BancaDetail.as_view(), name="banca_detail"),

    # URLs para Agendamento de Sala
    path("agendamentos-sala/", AgendamentoSalaList.as_view(), name="agendamento_sala_list"),
    path("agendamentos-sala/<int:pk>/", AgendamentoSalaDetail.as_view(), name="agendamento_sala_detail"),
]
