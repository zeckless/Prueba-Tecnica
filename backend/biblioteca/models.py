from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Categorías"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Prompt(models.Model):
    class Nivel(models.TextChoices):
        BASICA = "basica", "Educación básica"
        MEDIA = "media", "Educación media"
        UNIVERSITARIO = "universitario", "Universitario"
        TRANSVERSAL = "transversal", "Transversal"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente de revisión"
        APROBADO = "aprobado", "Aprobado"
        DESTACADO = "destacado", "Destacado por la comunidad"
        RECHAZADO = "rechazado", "Rechazado"

    titulo = models.CharField(max_length=180)
    descripcion = models.TextField(
        help_text="Para qué sirve el prompt y cómo se usa en clase."
    )
    contenido = models.TextField(help_text="Texto del prompt tal como se envía a la IA.")
    asignatura = models.CharField(max_length=120, blank=True)
    nivel = models.CharField(
        max_length=20, choices=Nivel.choices, default=Nivel.TRANSVERSAL
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="prompts"
    )
    tags = models.CharField(
        max_length=255, blank=True,
        help_text="Lista separada por comas. Ej: rúbrica, evaluación, escritura",
    )
    autor = models.CharField(max_length=120, default="Anónimo")
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PENDIENTE
    )
    likes = models.PositiveIntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en"]
        indexes = [models.Index(fields=["estado", "-creado_en"])]

    def __str__(self):
        return self.titulo

    def recalcular_destacado(self, umbral=5):
        if self.estado not in (self.Estado.APROBADO, self.Estado.DESTACADO):
            return
        nuevo = self.Estado.DESTACADO if self.likes >= umbral else self.Estado.APROBADO
        if nuevo != self.estado:
            self.estado = nuevo
            self.save(update_fields=["estado"])


class Comentario(models.Model):
    prompt = models.ForeignKey(
        Prompt, on_delete=models.CASCADE, related_name="comentarios"
    )
    autor = models.CharField(max_length=120, default="Anónimo")
    texto = models.TextField()
    contenido_sugerido = models.TextField(
        blank=True,
        help_text="Versión mejorada del prompt propuesta por la comunidad.",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["creado_en"]

    @property
    def es_propuesta_mejora(self):
        return bool(self.contenido_sugerido.strip())
