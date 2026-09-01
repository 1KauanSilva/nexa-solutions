from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status as http_status

from .models import Chamado
from .serializers import ChamadoSerializer


class ChamadoViewSet(viewsets.ModelViewSet):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer

    def list(self, request, *args, **kwargs):
        status_param = request.query_params.get("status")

        if status_param:
            status_param = status_param.upper()

            status_validos = [choice.value for choice in Chamado.Status]

            if status_param not in status_validos:
                return Response(
                    {
                        "detail": "Status inválido.",
                        "status_validos": status_validos,
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Chamado.objects.all()

        status_param = self.request.query_params.get("status")

        if status_param:
            status_param = status_param.upper()
            queryset = queryset.filter(status=status_param)

        return queryset