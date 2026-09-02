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

        self.assertEqual(response.data["total"], 4)
        self.assertEqual(response.data["abertos"], 2)
        self.assertEqual(response.data["em_andamento"], 1)
        self.assertEqual(response.data["concluidos"], 1)

    def test_indicadores_sem_chamados(self):
        url = reverse("indicadores")
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["total"], 0)
        self.assertEqual(response.data["abertos"], 0)
        self.assertEqual(response.data["em_andamento"], 0)
        self.assertEqual(response.data["concluidos"], 0)