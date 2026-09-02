from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChamadoViewSet, IndicadoresView


router = DefaultRouter()

router.register(
    r"chamados",
    ChamadoViewSet,
    basename="chamado",
)

urlpatterns = [
    path("", include(router.urls)),
    path("indicadores/", IndicadoresView.as_view(), name="indicadores"),
]