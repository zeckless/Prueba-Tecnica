from django.core.management.base import BaseCommand

from biblioteca.models import Categoria, Comentario, Prompt


class Command(BaseCommand):
    help = "Carga datos de ejemplo para la Biblioteca de prompts."

    def handle(self, *args, **options):
        categorias = {}
        for nombre in [
            "Evaluación",
            "Planificación de clases",
            "Retroalimentación",
            "Creación de material",
            "Investigación",
        ]:
            cat, _ = Categoria.objects.get_or_create(nombre=nombre)
            categorias[nombre] = cat

        ejemplos = [
            dict(
                titulo="Generar rúbrica para ensayo argumentativo",
                descripcion="Crea una rúbrica de 4 niveles para evaluar ensayos en 2° medio.",
                contenido=(
                    "Actúa como profesor/a de Lenguaje. Construye una rúbrica analítica "
                    "para evaluar un ensayo argumentativo de 800 palabras en 2° medio. "
                    "Incluye 4 niveles de logro y los criterios: tesis, argumentación, "
                    "uso de fuentes, cohesión y ortografía. Entrega el resultado en tabla."
                ),
                asignatura="Lenguaje y Comunicación",
                nivel=Prompt.Nivel.MEDIA,
                categoria=categorias["Evaluación"],
                tags="rúbrica, ensayo, evaluación",
                autor="Lucía Vergara",
                estado=Prompt.Estado.APROBADO,
            ),
            dict(
                titulo="Plan de clase de 90 minutos sobre fotosíntesis",
                descripcion="Diseña un plan de clase indagatorio para 7° básico.",
                contenido=(
                    "Eres docente de Ciencias Naturales. Diseña un plan de clase de 90 "
                    "minutos sobre fotosíntesis para 7° básico, con enfoque indagatorio. "
                    "Incluye objetivo de aprendizaje, activación de ideas previas, "
                    "experimento con plantas acuáticas, cierre metacognitivo y evaluación formativa."
                ),
                asignatura="Ciencias Naturales",
                nivel=Prompt.Nivel.BASICA,
                categoria=categorias["Planificación de clases"],
                tags="plan de clase, ciencias, indagación",
                autor="Juan Pizarro",
                estado=Prompt.Estado.APROBADO,
            ),
            dict(
                titulo="Retroalimentación personalizada a un informe de laboratorio",
                descripcion="Genera feedback constructivo en 3 párrafos.",
                contenido=(
                    "Lee el siguiente informe de laboratorio escrito por un/a estudiante "
                    "universitario/a de primer año de Ingeniería. Entrega retroalimentación "
                    "en 3 párrafos: (1) qué hizo bien, (2) qué debe mejorar con ejemplos "
                    "concretos del texto, (3) sugerencia de próximo paso. Usa tono amable y específico.\n\nINFORME:\n[pegar aquí]"
                ),
                asignatura="Ingeniería",
                nivel=Prompt.Nivel.UNIVERSITARIO,
                categoria=categorias["Retroalimentación"],
                tags="feedback, informe, universidad",
                autor="Lucía Vergara",
                estado=Prompt.Estado.DESTACADO,
                likes=7,
            ),
            dict(
                titulo="Generar 10 preguntas tipo PAES de comprensión lectora",
                descripcion="Crea ítems de selección múltiple con clave y justificación.",
                contenido=(
                    "A partir del siguiente texto, genera 10 preguntas de selección múltiple "
                    "estilo PAES (4 alternativas). Para cada una entrega: enunciado, alternativas, "
                    "clave correcta y breve justificación."
                ),
                asignatura="Lenguaje",
                nivel=Prompt.Nivel.MEDIA,
                categoria=categorias["Evaluación"],
                tags="PAES, comprensión lectora, ítems",
                autor="Juan Pizarro",
                estado=Prompt.Estado.PENDIENTE,
            ),
            dict(
                titulo="Resumir un paper académico para uso en clases",
                descripcion="Resume manteniendo precisión y citando.",
                contenido=(
                    "Eres asistente de investigación. Resume el siguiente paper en máximo "
                    "400 palabras para uso en una clase universitaria. Incluye: pregunta de "
                    "investigación, metodología, hallazgos clave, limitaciones y una cita "
                    "textual relevante con su número de página."
                ),
                asignatura="Transversal",
                nivel=Prompt.Nivel.UNIVERSITARIO,
                categoria=categorias["Investigación"],
                tags="resumen, paper, investigación",
                autor="Lucía Vergara",
                estado=Prompt.Estado.APROBADO,
            ),
        ]

        for data in ejemplos:
            Prompt.objects.get_or_create(titulo=data["titulo"], defaults=data)

        destacado = Prompt.objects.get(titulo__startswith="Retroalimentación personalizada")
        Comentario.objects.get_or_create(
            prompt=destacado,
            autor="Juan Pizarro",
            defaults={
                "texto": "Funciona muy bien. Sugiero pedir también un ejemplo reescrito de un párrafo.",
                "contenido_sugerido": (
                    "Lee el informe y entrega feedback en 3 párrafos. Adicionalmente, "
                    "reescribe un párrafo a modo de ejemplo."
                ),
            },
        )

        self.stdout.write(self.style.SUCCESS("Biblioteca: datos sembrados."))
