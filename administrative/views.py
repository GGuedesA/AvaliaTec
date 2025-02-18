from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Banca, AgendamentoSala, Block, Coordination, Room
from .serializers import (
    BancaSerializer,
    AgendamentoSalaSerializer,
    BlockSerializer,
    CoordinationSerializer,
    RoomSerializer,
)
from .forms import BlockForm, CoordinationForm, RoomForm, BancaForm, AgendamentoSalaForm
import json
from django.http import JsonResponse
from django.views.generic import ListView


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
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        form = BancaForm(data)
        if form.is_valid():
            banca = form.save(commit=False)
            banca.save()
            form.save_m2m()  # Save the many-to-many relationships
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = BancaForm()
    return render(request, "administrative/banca_form.html", {"form": form})


def create_agendamento(request):
    if request.method == "POST":
        form = AgendamentoSalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "administrative:agendamento_list"
            )  # Redirect to a list view or success page
    else:
        form = AgendamentoSalaForm()
    return render(request, "administrative/agendamento_form.html", {"form": form})


def get_salas(request):
    bloco = request.GET.get('bloco')
    if bloco:
        salas = Room.objects.filter(block__name__icontains=bloco)
        salas_data = [{"id": sala.id, "nome": sala.name} for sala in salas]
        return JsonResponse(salas_data, safe=False)
    return JsonResponse([], safe=False)


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
    

class SalaListView(ListView):
    model = AgendamentoSala
    template_name = "administrative/salas_list.html"
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
