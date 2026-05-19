from django.db.models import Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Categoria, Comentario, Prompt
from .serializers import CategoriaSerializer, ComentarioSerializer, PromptSerializer


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class PromptViewSet(viewsets.ModelViewSet):
    serializer_class = PromptSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["categoria", "nivel", "estado", "asignatura"]
    search_fields = ["titulo", "descripcion", "contenido", "tags", "asignatura"]
    ordering_fields = ["creado_en", "likes"]

    def get_queryset(self):
        qs = (
            Prompt.objects.select_related("categoria")
            .annotate(total_comentarios=Count("comentarios", distinct=True))
        )
        if self.action == "list" and "estado" not in self.request.query_params:
            qs = qs.filter(estado__in=[Prompt.Estado.APROBADO, Prompt.Estado.DESTACADO])
        return qs

    def perform_create(self, serializer):
        serializer.save(estado=Prompt.Estado.APROBADO)

    @action(detail=True, methods=["post"])
    def votar(self, request, pk=None):
        prompt = self.get_object()
        if prompt.estado not in (Prompt.Estado.APROBADO, Prompt.Estado.DESTACADO):
            return Response(
                {"detail": "Solo se pueden votar prompts aprobados."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Prompt.objects.filter(pk=prompt.pk).update(likes=F("likes") + 1)
        prompt.refresh_from_db()
        prompt.recalcular_destacado()
        return Response({"likes": prompt.likes, "estado": prompt.estado})

    @action(detail=True, methods=["post"])
    def aprobar(self, request, pk=None):
        prompt = self.get_object()
        prompt.estado = Prompt.Estado.APROBADO
        prompt.save(update_fields=["estado"])
        prompt.recalcular_destacado()
        return Response({"estado": prompt.estado})

    @action(detail=True, methods=["post"])
    def rechazar(self, request, pk=None):
        prompt = self.get_object()
        prompt.estado = Prompt.Estado.RECHAZADO
        prompt.save(update_fields=["estado"])
        return Response({"estado": prompt.estado})

    @action(detail=True, methods=["get", "post"], url_path="comentarios")
    def comentarios(self, request, pk=None):
        prompt = self.get_object()
        if request.method == "GET":
            qs = prompt.comentarios.all()
            return Response(ComentarioSerializer(qs, many=True).data)
        s = ComentarioSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        comentario = Comentario.objects.create(
            prompt=prompt,
            autor=s.validated_data.get("autor") or "Anónimo",
            texto=s.validated_data["texto"],
            contenido_sugerido=s.validated_data.get("contenido_sugerido", ""),
        )
        return Response(
            ComentarioSerializer(comentario).data, status=status.HTTP_201_CREATED
        )
