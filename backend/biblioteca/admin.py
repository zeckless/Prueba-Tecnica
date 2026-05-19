from django.contrib import admin

from .models import Categoria, Comentario, Prompt


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    readonly_fields = ("creado_en",)


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "categoria", "nivel", "estado", "likes", "creado_en")
    list_filter = ("estado", "nivel", "categoria")
    search_fields = ("titulo", "descripcion", "contenido", "tags", "asignatura", "autor")
    actions = ["aprobar_prompts", "rechazar_prompts"]
    inlines = [ComentarioInline]

    @admin.action(description="Aprobar prompts seleccionados")
    def aprobar_prompts(self, request, queryset):
        for p in queryset:
            p.estado = Prompt.Estado.APROBADO
            p.save(update_fields=["estado"])
            p.recalcular_destacado()

    @admin.action(description="Rechazar prompts seleccionados")
    def rechazar_prompts(self, request, queryset):
        queryset.update(estado=Prompt.Estado.RECHAZADO)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("prompt", "autor", "es_propuesta_mejora", "creado_en")
