from django.urls import path

from .views import ChamadoDetailView, ChamadoListCreateView

urlpatterns = [
    path(
        "chamados/",
        ChamadoListCreateView.as_view(),
        name="chamado-list-create",
    ),
    path(
        "chamados/<int:pk>/",
        ChamadoDetailView.as_view(),
        name="chamado-detail",
    ),
]