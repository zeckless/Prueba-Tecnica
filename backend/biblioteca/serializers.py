from rest_framework import serializers

from .models import Categoria, Comentario, Prompt


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "slug"]
        read_only_fields = ["slug"]


class ComentarioSerializer(serializers.ModelSerializer):
    es_propuesta_mejora = serializers.BooleanField(read_only=True)

    class Meta:
        model = Comentario
        fields = [
            "id", "prompt", "autor", "texto",
            "contenido_sugerido", "es_propuesta_mejora", "creado_en",
        ]
        read_only_fields = ["prompt", "creado_en"]


class PromptSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)
    total_comentarios = serializers.IntegerField(read_only=True)
    tags_lista = serializers.SerializerMethodField()

    class Meta:
        model = Prompt
        fields = [
            "id", "titulo", "descripcion", "contenido",
            "asignatura", "nivel", "categoria", "categoria_nombre",
            "tags", "tags_lista", "autor", "estado", "likes",
            "total_comentarios",
            "creado_en", "actualizado_en",
        ]
        read_only_fields = ["estado", "likes", "creado_en", "actualizado_en"]

    def get_tags_lista(self, obj):
        return [t.strip() for t in obj.tags.split(",") if t.strip()]
