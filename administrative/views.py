from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Banca, AgendamentoSala
from .serializers import BancaSerializer, AgendamentoSalaSerializer


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
