from django.core.management.base import BaseCommand

from community.models import Discussion, PromptActivity, Resource


class Command(BaseCommand):
    help = "Carga datos demo para el prototipo de comunidad docente."

    def handle(self, *args, **options):
        PromptActivity.objects.all().delete()
        Resource.objects.all().delete()
        Discussion.objects.all().delete()

        PromptActivity.objects.bulk_create(
            [
                PromptActivity(
                    title="Diseño de rúbricas con criterios transparentes",
                    summary="Actividad para que estudiantes contrasten una rúbrica generada por IA con criterios del curso.",
                    prompt="Actúa como asesor pedagógico. Propón una rúbrica analítica para evaluar [producto] en [curso], con cuatro criterios, niveles de desempeño y lenguaje claro para estudiantes.",
                    subject="Evaluación",
                    level="Universidad",
                    author="María González",
                    status="curated",
                    tags="rubricas, evaluación, transparencia",
                    likes=28,
                ),
                PromptActivity(
                    title="Debate guiado sobre sesgos de IA",
                    summary="Secuencia de preguntas para discutir sesgos algorítmicos usando casos cercanos a la disciplina.",
                    prompt="Genera un caso breve sobre sesgo en IA aplicado a [disciplina]. Incluye preguntas de discusión, contraargumentos y una pauta para cierre reflexivo.",
                    subject="Ética",
                    level="Docentes",
                    author="Equipo Oficina IA",
                    status="curated",
                    tags="ética, sesgos, discusión",
                    likes=34,
                ),
                PromptActivity(
                    title="Tutor socrático para lectura académica",
                    summary="Prompt para transformar un texto complejo en una conversación de comprensión progresiva.",
                    prompt="Ayúdame a guiar a estudiantes que leen este texto: [fragmento]. No entregues respuestas directas; formula preguntas graduadas y detecta malentendidos comunes.",
                    subject="Lectura",
                    level="Colegio",
                    author="Camila Rojas",
                    status="review",
                    tags="lectura, tutoría, pensamiento crítico",
                    likes=16,
                ),
                PromptActivity(
                    title="Planificación de clase con uso responsable de IA",
                    summary="Plantilla para diseñar una clase que incluya IA generativa y explicite límites, evidencias y evaluación.",
                    prompt="Diseña una clase de 90 minutos sobre [tema]. Incluye objetivo, actividad con IA, resguardos éticos, evidencia de aprendizaje y adaptación para distintos niveles.",
                    subject="Planificación",
                    level="Docentes",
                    author="Felipe Araya",
                    status="curated",
                    tags="planificación, IA generativa, clase",
                    likes=41,
                ),
            ]
        )

        Resource.objects.bulk_create(
            [
                Resource(
                    title="Cursos abiertos de la Oficina de IA",
                    description="Ruta inicial para alfabetización docente en IA generativa, uso responsable y diseño de actividades.",
                    resource_type="course",
                    source="Oficina de IA - VTI Universidad de Chile",
                    url="https://vti-ia.uchile.cl/iniciativas/",
                    image_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
                    featured=True,
                ),
                Resource(
                    title="Programas CIAE para innovación educativa",
                    description="Materiales y programas de apoyo para comunidades docentes y mejora de prácticas pedagógicas.",
                    resource_type="program",
                    source="CIAE",
                    url="https://www.ciae.uchile.cl/",
                    image_url="https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?auto=format&fit=crop&w=1200&q=80",
                    featured=True,
                ),
                Resource(
                    title="Webinar: Aprender jugando",
                    description="Evidencia y experiencias para fortalecer el juego en el aula, orientado a prácticas pedagógicas activas.",
                    resource_type="program",
                    source="CIAE Universidad de Chile",
                    url="https://www.ciae.uchile.cl/evento/webinar-aprender-jugando-evidencia-y-experiencias-para-fortalecer-el-juego-en-el-aula",
                    image_url="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1200&q=80",
                    label="Webinar",
                    event_date="Fecha por confirmar",
                    featured=True,
                    sort_order=100,
                ),
                Resource(
                    title="Guía de curación de prompts",
                    description="Criterios base para revisar propósito, reproducibilidad, sesgos, privacidad y alineación curricular.",
                    resource_type="guide",
                    source="Comunidad docente IA",
                    image_url="https://images.unsplash.com/photo-1456324504439-367cee3b3c32?auto=format&fit=crop&w=1200&q=80",
                    featured=True,
                ),
                Resource(
                    title="Sitio institucional Oficina de IA",
                    description="Punto de entrada a noticias, actividades y materiales oficiales de la iniciativa.",
                    resource_type="site",
                    source="VTI Universidad de Chile",
                    url="https://vti-ia.uchile.cl/",
                    image_url="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1200&q=80",
                    featured=False,
                ),
                Resource(
                    title="Vicerrectoría de Tecnologías de la Información",
                    description="Sitio oficial de la VTI Universidad de Chile con información institucional, innovación y transformación digital.",
                    resource_type="site",
                    source="Universidad de Chile",
                    url="https://vti.uchile.cl/",
                    image_url="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
                    featured=False,
                ),
                Resource(
                    title="Claude Code in Action",
                    description="Curso de referencia para observar cómo estructurar aprendizaje práctico, progresivo y orientado a casos de uso con asistentes de código.",
                    resource_type="course",
                    source="Anthropic Academy",
                    url="https://anthropic.skilljar.com/claude-code-in-action",
                    image_url="https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=1200&q=80",
                    featured=False,
                ),
            ]
        )

        Discussion.objects.bulk_create(
            [
                Discussion(
                    title="¿Cómo declarar el uso de IA en evaluaciones?",
                    body="Buscamos acuerdos mínimos para que estudiantes documenten cuándo usaron IA y qué decisiones tomaron.",
                    author="Daniela Pérez",
                    topic="Evaluación",
                    replies=12,
                ),
                Discussion(
                    title="Banco de ejemplos para ciencias sociales",
                    body="Estoy reuniendo actividades probadas en cursos de metodología y análisis de datos cualitativos.",
                    author="Jorge Muñoz",
                    topic="Actividades",
                    replies=8,
                ),
                Discussion(
                    title="Privacidad al trabajar con datos de estudiantes",
                    body="Propongo levantar una lista de chequeo antes de usar herramientas externas con información sensible.",
                    author="Sofía Herrera",
                    topic="Ética",
                    replies=15,
                ),
            ]
        )

        self.stdout.write(self.style.SUCCESS("Datos demo cargados."))
