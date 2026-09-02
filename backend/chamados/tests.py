from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Chamado


class ChamadoTests(APITestCase):

    def test_criar_chamado_valido(self):
        dados = {
            "titulo": "Chamado de teste",
            "descricao": "Descrição do chamado de teste",
            "status": "ABERTO",
        }

        response = self.client.post(
            "/api/chamados/",
            dados,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["titulo"],
            "Chamado de teste",
        )

        self.assertEqual(
            response.data["status"],
            "ABERTO",
        )

    def test_criar_chamado_sem_titulo(self):
        dados = {
            "descricao": "Chamado sem título para teste",
            "status": "ABERTO",
        }

        response = self.client.post(
            "/api/chamados/",
            dados,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "titulo",
            response.data,
        )

    def test_filtrar_chamados_por_status(self):
        Chamado.objects.create(
            titulo="Chamado aberto",
            descricao="Descrição do chamado aberto",
            status=Chamado.Status.ABERTO,
        )

        Chamado.objects.create(
            titulo="Chamado concluído",
            descricao="Descrição do chamado concluído",
            status=Chamado.Status.CONCLUIDO,
        )

        response = self.client.get(
            "/api/chamados/?status=ABERTO"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["titulo"],
            "Chamado aberto",
        )

        self.assertEqual(
            response.data[0]["status"],
            "ABERTO",
        )


class IndicadoresTests(APITestCase):

    def test_indicadores_com_chamados(self):
        Chamado.objects.create(
            titulo="Chamado aberto",
            status=Chamado.Status.ABERTO,
        )

        Chamado.objects.create(
            titulo="Chamado em andamento",
            status=Chamado.Status.EM_ANDAMENTO,
        )

        Chamado.objects.create(
            titulo="Chamado concluído",
            status=Chamado.Status.CONCLUIDO,
        )

        Chamado.objects.create(
            titulo="Outro chamado aberto",
            status=Chamado.Status.ABERTO,
        )

        url = reverse("indicadores")
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["total"],
            4,
        )

        self.assertEqual(
            response.data["abertos"],
            2,
        )

        self.assertEqual(
            response.data["em_andamento"],
            1,
        )

        self.assertEqual(
            response.data["concluidos"],
            1,
        )

    def test_indicadores_sem_chamados(self):
        url = reverse("indicadores")
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["total"],
            0,
        )

        self.assertEqual(
            response.data["abertos"],
            0,
        )

        self.assertEqual(
            response.data["em_andamento"],
            0,
        )

        self.assertEqual(
            response.data["concluidos"],
            0,
        )