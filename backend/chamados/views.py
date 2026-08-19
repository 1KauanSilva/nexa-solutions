from rest_framework import generics

from .models import Chamado
from .serializers import ChamadoSerializer


class ChamadoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria chamados.

    Limitações intencionais:
    - Não filtra chamados por status.
    - Não oferece indicadores.
    - Não há tratamento adicional para parâmetros inválidos.
    """

    queryset = Chamado.objects.all().order_by("-criado_em")
    serializer_class = ChamadoSerializer


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer