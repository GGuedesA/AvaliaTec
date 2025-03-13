from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from accounts.models import Usuario
from .models import Banca, AgendamentoSala, Block, Coordination, Room
from .serializers import (
    BancaSerializer,
    AgendamentoSalaSerializer,
    BlockSerializer,
    CoordinationSerializer,
    RoomSerializer,
)
from .forms import BlockForm, CoordinationForm, RoomForm, BancaForm, AgendamentoSalaForm

from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes


def banca(request):
    return render(request, "administrative/banca.html")


def create_block(request):
    if request.method == "POST":
        form = BlockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "administrative:block_list"
            )  # Redirect to a list view or success page
    else:
        form = BlockForm()
    return render(request, "administrative/block_form.html", {"form": form})


def create_coordination(request):
    if request.method == "POST":
        form = CoordinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "administrative:coordination_list"
            )  # Redirect to a list view or success page
    else:
        form = CoordinationForm()
    return render(request, "administrative/coordination_form.html", {"form": form})


def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "administrative:room_list"
            )  # Redirect to a list view or success page
    else:
        form = RoomForm()
    return render(request, "administrative/room_form.html", {"form": form})


def create_banca(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Pegando JSON da requisição

            # Validations
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            selected_date = datetime.strptime(data["data"], "%Y-%m-%d").date()
            selected_horario_inicio = datetime.strptime(
                data["horario_inicio"], "%H:%M"
            ).time()
            selected_horario_fim = datetime.strptime(
                data["horario_fim"], "%H:%M"
            ).time()

            if selected_date < current_date and request.user.role != "secretary":
                return JsonResponse(
                    {
                        "success": False,
                        "errors": "Você não pode criar bancas antes do dia atual.",
                    },
                    status=400,
                )

            if (
                selected_date == current_date
                and selected_horario_inicio < current_time
                and request.user.role != "secretary"
            ):
                return JsonResponse(
                    {
                        "success": False,
                        "errors": "Você não pode criar bancas em horário anterior ao atual.",
                    },
                    status=400,
                )

            if selected_horario_inicio >= selected_horario_fim:
                return JsonResponse(
                    {
                        "success": False,
                        "errors": "O horário de início não pode ser superior ao horário de fim.",
                    },
                    status=400,
                )

            # Criando a instância do formulário com os dados recebidos
            form = BancaForm(data)
            if form.is_valid():
                banca = form.save(commit=False)

                # Salvando os relacionamentos baseados nos IDs recebidos
                banca.orientador = Usuario.objects.get(id=data["orientador"])
                banca.co_orientador = (
                    Usuario.objects.get(id=data["co_orientador"])
                    if data["co_orientador"]
                    else None
                )
                banca.sala = Room.objects.get(id=data["sala"])
                banca.block = Block.objects.get(id=data["bloco"])
                banca.coordination = Coordination.objects.get(id=data["coordination"])

                banca.save()

                # Adicionando professores da banca
                banca.professores_banca.set(
                    Usuario.objects.filter(id__in=data["professores_banca"])
                )

                return JsonResponse({"success": True}, status=201)
            else:
                # Log form errors for debugging
                print("Form errors:", form.errors)
                return JsonResponse(
                    {"success": False, "errors": form.errors}, status=400
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "errors": "Invalid JSON"}, status=400
            )

    else:
        form = BancaForm()
        orientadores = Usuario.objects.filter(role=Usuario.RoleChoices.TEACHER)
        co_orientadores = Usuario.objects.filter(role=Usuario.RoleChoices.TEACHER)
        professores_banca = Usuario.objects.filter(role=Usuario.RoleChoices.TEACHER)
        blocks = Block.objects.all()

        return render(
            request,
            "administrative/banca_form.html",
            {
                "form": form,
                "orientadores": orientadores,
                "co_orientadores": co_orientadores,
                "professores_banca": professores_banca,
                "blocks": blocks,
            },
        )


def create_agendamento(request):
    if request.method == "POST":
        form = AgendamentoSalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administrative:agendamento_list")
    else:
        form = AgendamentoSalaForm()
    professores = Usuario.objects.filter(role=Usuario.RoleChoices.TEACHER)
    salas = Room.objects.all()
    return render(
        request,
        "administrative/agendamento_form.html",
        {"form": form, "professores": professores, "salas": salas},
    )


def get_salas(request):
    bloco = request.GET.get("bloco")
    if bloco:
        salas = Room.objects.filter(block__name__icontains=bloco)
        salas_data = [{"id": sala.id, "nome": sala.name} for sala in salas]
        return JsonResponse(salas_data, safe=False)
    return JsonResponse([], safe=False)


def get_orientadores(request):
    term = request.GET.get("term", "")
    orientadores = Usuario.objects.filter(
        name__icontains=term, role=Usuario.RoleChoices.TEACHER
    )
    orientadores_list = list(orientadores.values("id", "name"))
    return JsonResponse(orientadores_list, safe=False)


def get_salas_por_bloco(request):
    bloco_id = request.GET.get("bloco_id")
    if bloco_id:
        salas = Room.objects.filter(block_id=bloco_id)
        salas_data = [{"id": sala.id, "nome": sala.name} for sala in salas]
        return JsonResponse(salas_data, safe=False)
    return JsonResponse([], safe=False)


def get_blocos(request):
    term = request.GET.get("term", "")
    blocos = Block.objects.filter(name__icontains=term)
    blocos_list = list(blocos.values("id", "name"))
    return JsonResponse(blocos_list, safe=False)


def get_professores(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        q = request.GET.get("term", "")
        professores = Usuario.objects.filter(
            name__icontains=q, role=Usuario.RoleChoices.TEACHER
        )
        results = []
        for professor in professores:
            professor_json = {}
            professor_json["id"] = professor.id
            professor_json["label"] = professor.name
            professor_json["value"] = professor.name
            results.append(professor_json)
        return JsonResponse(results, safe=False)
    return JsonResponse({"error": "Invalid request"}, status=400)


# ==================== Views para Banca ====================
class BancaList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Lista todas as bancas (com filtro opcional por tema ou tipo)."""
        q = request.query_params.get("search", "")
        bancas = Banca.objects.filter(tema__icontains=q)  # Filtro simples pelo tema
        serializer = BancaSerializer(bancas, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Cria uma nova banca de defesa ou TCC."""
        serializer = BancaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BancaDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Retorna os detalhes de uma banca específica."""
        banca = get_object_or_404(Banca, pk=pk)
        serializer = BancaSerializer(banca)
        return Response(serializer.data)

    def put(self, request, pk):
        """Atualiza uma banca existente, com regras de permissão baseadas no status."""
        banca = get_object_or_404(Banca, pk=pk)

        # Verifica se o status da banca é "confirmado", nesse caso só o secretário pode atualizar
        if banca.status == Banca.StatusAgendamento.CONFIRMADO:
            if request.user.role != "secretary":
                return Response(
                    {
                        "detail": "Somente secretários podem atualizar bancas com status confirmado."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        # Atualização do objeto
        serializer = BancaSerializer(banca, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Deleta uma banca existente."""
        banca = get_object_or_404(Banca, pk=pk)

        # Verifica se o status da banca é "confirmado", e somente o secretário pode deletar
        if banca.status == Banca.StatusAgendamento.CONFIRMADO:
            if request.user.role != "secretary":
                return Response(
                    {
                        "detail": "Somente secretários podem deletar bancas com status confirmado."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        banca.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BancaListView(ListView):
    model = Banca
    template_name = "administrative/banca_list.html"
    context_object_name = "bancas"
    paginate_by = 10  # Opcional: para adicionar paginação

    def get_queryset(self):
        user = self.request.user
        user_role = user.role  # Obtém o tipo de usuário

        if user_role == "secretary":
            # Secretários veem bancas relacionadas à sua coordenação
            bancas = Banca.objects.filter(coordination=user.coordination)
        else:
            # Professores veem bancas onde estão envolvidos
            bancas = Banca.objects.filter(
                Q(professores_banca=user) | Q(orientador=user) | Q(co_orientador=user)
            )

        bancas = bancas.order_by("data")  # Ordena por data
        for banca in bancas:
            banca.update_status()
        return bancas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_role"] = (
            self.request.user.role
        )  # Adiciona o tipo de usuário ao contexto
        return context


class SalaListView(ListView):
    model = AgendamentoSala
    template_name = "administrative/agendamento_list.html"
    context_object_name = "agendamentos"
    paginate_by = 10


# ==================== Views para Agendamento ====================
class AgendamentoSalaList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Lista todos os agendamentos de sala, com filtro opcional por matéria ou sala."""
        q = request.query_params.get("search", "")
        agendamentos = AgendamentoSala.objects.filter(
            materia__icontains=q
        )  # Filtro simples pela matéria
        serializer = AgendamentoSalaSerializer(agendamentos, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Cria um novo agendamento de sala."""
        serializer = AgendamentoSalaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgendamentoSalaDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Retorna os detalhes de um agendamento de sala específico."""
        agendamento = get_object_or_404(AgendamentoSala, pk=pk)
        serializer = AgendamentoSalaSerializer(agendamento)
        return Response(serializer.data)

    def put(self, request, pk):
        """Atualiza um agendamento de sala, com regras de permissão baseadas no status."""
        agendamento = get_object_or_404(AgendamentoSala, pk=pk)

        # Verifica se o status do agendamento é "confirmado", e somente o secretário pode atualizar
        if agendamento.status == AgendamentoSala.StatusAgendamento.CONFIRMADO:
            if request.user.role != "secretary":
                return Response(
                    {
                        "detail": "Somente secretários podem atualizar agendamentos com status confirmado."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        # Atualização do objeto
        serializer = AgendamentoSalaSerializer(
            agendamento, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Deleta um agendamento de sala existente."""
        agendamento = get_object_or_404(AgendamentoSala, pk=pk)

        # Verifica se o status do agendamento é "confirmado", e somente o secretário pode deletar
        if agendamento.status == AgendamentoSala.StatusAgendamento.CONFIRMADO:
            if request.user.role != "secretary":
                return Response(
                    {
                        "detail": "Somente secretários podem deletar agendamentos com status confirmado."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        agendamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgendamentoSalaListView(ListView):
    model = AgendamentoSala
    template_name = "administrative/agendamento_list.html"
    context_object_name = "agendamentos"


# ==================== Views para Block ====================
class BlockList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Lista todos os blocos"""
        blocks = Block.objects.all()
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Cria um novo bloco"""
        serializer = BlockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Retorna os detalhes de um bloco"""
        block = get_object_or_404(Block, pk=pk)
        serializer = BlockSerializer(block)
        return Response(serializer.data)

    def put(self, request, pk):
        """Atualiza um bloco existente"""
        block = get_object_or_404(Block, pk=pk)
        serializer = BlockSerializer(block, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Remove um bloco"""
        block = get_object_or_404(Block, pk=pk)
        block.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Views para Coordination ====================
class CoordinationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Lista todas as coordenações"""
        coordinations = Coordination.objects.all()
        serializer = CoordinationSerializer(coordinations, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Cria uma nova coordenação"""
        serializer = CoordinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoordinationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Retorna os detalhes de uma coordenação"""
        coordination = get_object_or_404(Coordination, pk=pk)
        serializer = CoordinationSerializer(coordination)
        return Response(serializer.data)

    def put(self, request, pk):
        """Atualiza uma coordenação existente"""
        coordination = get_object_or_404(Coordination, pk=pk)
        serializer = CoordinationSerializer(
            coordination, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Remove uma coordenação"""
        coordination = get_object_or_404(Coordination, pk=pk)
        coordination.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Views para Room ====================
class RoomList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Cria uma nova sala"""
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Retorna os detalhes de uma sala"""
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        """Atualiza uma sala existente"""
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Remove uma sala"""
        room = get_object_or_404(Room, pk=pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def edit_banca(request, pk):
    banca = get_object_or_404(Banca, pk=pk)
    if request.method == "POST":
        form = BancaForm(request.POST, instance=banca)
        if form.is_valid():
            form.save()
            return redirect("listar_bancas")
    else:
        form = BancaForm(instance=banca)
    return render(request, "administrative/banca_form.html", {"form": form})


@csrf_exempt
def confirm_banca(request, banca_id):
    if request.method == "POST":
        try:
            banca = Banca.objects.get(id=banca_id)
            banca.status = Banca.StatusBanca.ACEITA
            banca.save()
            return JsonResponse({"success": True})
        except Banca.DoesNotExist:
            return JsonResponse({"success": False, "error": "Banca não encontrada."})
    return JsonResponse({"success": False, "error": "Método não permitido."})


@csrf_exempt
def confirm_agendamento(request, agendamento_id):
    if request.method == "POST":
        try:
            agendamento = AgendamentoSala.objects.get(id=agendamento_id)
            agendamento.status = AgendamentoSala.StatusAgendamento.CONFIRMADO
            agendamento.save()
            return JsonResponse({"success": True})
        except AgendamentoSala.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Agendamento não encontrado."}
            )
    return JsonResponse({"success": False, "error": "Método não permitido."})


def generate_pdf(request, banca_id, user_id):
    banca = Banca.objects.get(id=banca_id)
    user = Usuario.objects.get(id=user_id)

    pdf_filename = f"declaracao_banca_{banca.id}.pdf"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pdf_filename}"'

    # Criação do PDF
    p = canvas.Canvas(response, pagesize=A4)

    # Dimensões
    width, height = A4
    margin_x = 50
    y = height - 50  # Coordenada inicial do topo

    # Cabeçalho
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, y, "UNIVERSIDADE FEDERAL DO ACRE")
    y -= 20
    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2, y, "CENTRO DE CIÊNCIAS EXATAS E TECNOLÓGICAS")
    y -= 20
    p.drawCentredString(
        width / 2, y, "COORDENAÇÃO DO CURSO DE BACHARELADO EM SISTEMAS DE INFORMAÇÃO"
    )
    y -= 40

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, y, "DECLARAÇÃO")
    y -= 40

    # Corpo do texto
    p.setFont("Helvetica", 12)
    text = f"""
    Processo nº 23107.006644/2025-02
    Interessado: {user.get_full_name()}

    Declaramos, para os devidos fins e efeitos legais, que o(a) {user.get_full_name()}, na condição
    de {user.role}, participou da banca de apresentação do Trabalho de Conclusão de Curso
    intitulado "{banca.tema if banca.tema else "Tema não informado"}"
    do discente {banca.alunos_nomes if banca.alunos_nomes else "Aluno não informado"}, apresentado em 10 de março de 2025.
    """
    # Inserindo o texto no PDF, linha por linha
    for linha in text.strip().split("\n"):
        p.drawString(margin_x, y, linha.strip())
        y -= 20

    # Professores da banca
    if banca.professores_banca.exists():
        y -= 20
        p.drawString(margin_x, y, "Demais componentes da banca:")
        y -= 20
        professores_nomes = [
            f"{professor.get_full_name()} - Membro"
            for professor in banca.professores_banca.all()
        ]
        for nome in professores_nomes:
            p.drawString(margin_x, y, nome)
            y -= 20

    # Data à direita
    data = "Rio Branco/AC, 12 de março de 2025"
    p.drawRightString(width - margin_x, y, data)
    y -= 220  # Espaço após a data

    # Rodapé centralizado
    rodape = """
    GEIRTO DE SOUZA
    Coordenador de Curso, pró tempore
    """
    for linha in rodape.strip().split("\n"):
        p.drawCentredString(width / 2, y, linha.strip())
        y -= 20

    # Finaliza o PDF
    p.showPage()
    p.save()

    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def historico(request):
    user = request.user
    user_role = user.role  # Obtém o tipo de usuário

    if user_role == "secretary":
        # Secretários veem bancas relacionadas à sua coordenação
        bancas = Banca.objects.filter(
            status="finalizada", coordination=user.fk_coordination
        )
    else:
        # Outros usuários veem bancas onde estão envolvidos
        bancas = Banca.objects.filter(status="finalizada").filter(
            Q(professores_banca=user) | Q(orientador=user) | Q(co_orientador=user)
        )

    bancas = bancas.select_related(
        "sala__block", "orientador", "co_orientador"
    ).prefetch_related("professores_banca")

    bancas_data = [
        {
            "id": banca.id,
            "tema": banca.tema,
            "data": banca.data,
            "alunos_nomes": banca.alunos_nomes,
            "sala": banca.sala,
            "horario_inicio": banca.horario_inicio,
            "horario_fim": banca.horario_fim,
            "status": banca.status,
            "orientador": banca.orientador,
            "co_orientador": banca.co_orientador,
            "professores_banca": banca.professores_banca.all(),
        }
        for banca in bancas
    ]
    return render(
        request,
        "administrative/historico.html",
        {"bancas": bancas_data, "user_role": user_role},
    )
