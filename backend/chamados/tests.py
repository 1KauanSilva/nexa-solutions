from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Chamado


class ChamadoFiltroStatusTests(APITestCase):

    def setUp(self):
        self.chamado_aberto = Chamado.objects.create(
            titulo="Chamado aberto",
            descricao="Teste de chamado aberto",
            status=Chamado.Status.ABERTO,
        )

        self.chamado_andamento = Chamado.objects.create(
            titulo="Chamado em andamento",
            descricao="Teste de chamado em andamento",
            status=Chamado.Status.EM_ANDAMENTO,
        )

        self.chamado_concluido = Chamado.objects.create(
            titulo="Chamado concluído",
            descricao="Teste de chamado concluído",
            status=Chamado.Status.CONCLUIDO,
        )

    def test_filtrar_chamados_por_status_aberto(self):
        url = reverse("chamado-list")

        response = self.client.get(
            url,
            {"status": "ABERTO"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["status"],
            Chamado.Status.ABERTO,
        )

    def test_sem_filtro_retorna_todos_os_chamados(self):
        url = reverse("chamado-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 3)

    def test_status_invalido_retorna_erro_400(self):
        url = reverse("chamado-list")

        response = self.client.get(
            url,
            {"status": "INVALIDO"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            response.data["detail"],
            "Status inválido.",
        )