from django.db import models


class PromptActivity(models.Model):
    STATUS_CHOICES = [
        ("curated", "Curado"),
        ("review", "En revision"),
        ("draft", "Borrador"),
    ]

    title = models.CharField(max_length=180)
    summary = models.TextField()
    prompt = models.TextField()
    subject = models.CharField(max_length=90)
    level = models.CharField(max_length=90)
    author = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="review")
    tags = models.CharField(max_length=220, blank=True)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Resource(models.Model):
    TYPE_CHOICES = [
        ("course", "Curso"),
        ("program", "Programa"),
        ("site", "Sitio"),
        ("guide", "Guia"),
    ]

    title = models.CharField(max_length=180)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    label = models.CharField(max_length=80, blank=True)
    event_date = models.CharField(max_length=80, blank=True)
    source = models.CharField(max_length=120)
    featured = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sort_order", "-featured", "title"]

    def __str__(self):
        return self.title


class Discussion(models.Model):
    title = models.CharField(max_length=180)
    body = models.TextField()
    author = models.CharField(max_length=120)
    topic = models.CharField(max_length=90)
    replies = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_activity"]

    def __str__(self):
        return self.title
