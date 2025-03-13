from django.urls import path
from .views import (
    BancaList,
    BancaDetail,
    AgendamentoSalaList,
    AgendamentoSalaDetail,
    BlockList,
    BlockDetail,
    CoordinationList,
    CoordinationDetail,
    RoomList,
    RoomDetail,
    create_block,
    create_coordination,
    create_room,
    create_banca,
    create_agendamento,
    BancaListView,
    banca,
    get_salas,
    SalaListView,
    get_orientadores,
    get_salas_por_bloco,
    get_blocos,
    confirm_banca,
    edit_banca,
    generate_pdf,
    AgendamentoSalaListView,
    get_professores,
    confirm_agendamento,
    historico,
)

app_name = "administrative"
urlpatterns = [
    path("banca/", banca, name="banca"),
    path("bancas/", BancaList.as_view(), name="banca_list"),
    path("bancas/<int:pk>/", BancaDetail.as_view(), name="banca_detail"),
    path("bancas/<int:pk>/edit/", edit_banca, name="edit_banca"),
    path("agendamentos/", AgendamentoSalaList.as_view(), name="agendamento_list"),
    path(
        "agendamentos/<int:pk>/",
        AgendamentoSalaDetail.as_view(),
        name="agendamento_detail",
    ),
    path("blocks/", BlockList.as_view(), name="block_list"),
    path("blocks/<int:pk>/", BlockDetail.as_view(), name="block_detail"),
    path("coordinations/", CoordinationList.as_view(), name="coordination_list"),
    path(
        "coordinations/<int:pk>/",
        CoordinationDetail.as_view(),
        name="coordination_detail",
    ),
    path("rooms/", RoomList.as_view(), name="room_list"),
    path("rooms/<int:pk>/", RoomDetail.as_view(), name="room_detail"),
    path("create_block/", create_block, name="create_block"),
    path("create_coordination/", create_coordination, name="create_coordination"),
    path("create_room/", create_room, name="create_room"),
    path("create_banca/", create_banca, name="create_banca"),
    path("create_agendamento/", create_agendamento, name="create_agendamento"),
    path("bancas/listar/", BancaListView.as_view(), name="listar_bancas"),
    path("salas/listar/", SalaListView.as_view(), name="listar_salas"),
    path("salas/", get_salas, name="get_salas"),
    path("get_orientadores/", get_orientadores, name="get_orientadores"),
    path("get_salas_por_bloco/", get_salas_por_bloco, name="get_salas_por_bloco"),
    path("get_blocos/", get_blocos, name="get_blocos"),
    path("confirm_banca/<int:banca_id>/", confirm_banca, name="confirm_banca"),
    path(
        "generate_pdf/<int:banca_id>/<int:user_id>/", generate_pdf, name="generate_pdf"
    ),
    path(
        "agendamentos/listar/",
        AgendamentoSalaListView.as_view(),
        name="agendamento_list",
    ),
    path("get_professores/", get_professores, name="get_professores"),
    path(
        "confirm_agendamento/<int:agendamento_id>/",
        confirm_agendamento,
        name="confirm_agendamento",
    ),
    path("historico/", historico, name="historico"),
]
