import json

from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Discussion, PromptActivity, Resource


def _tags(value):
    return [tag.strip() for tag in value.split(",") if tag.strip()]


def _prompt_payload(prompt):
    return {
        "id": prompt.id,
        "title": prompt.title,
        "summary": prompt.summary,
        "prompt": prompt.prompt,
        "subject": prompt.subject,
        "level": prompt.level,
        "author": prompt.author,
        "status": prompt.status,
        "tags": _tags(prompt.tags),
        "likes": prompt.likes,
        "createdAt": prompt.created_at.isoformat(),
    }


def _resource_payload(resource):
    return {
        "id": resource.id,
        "title": resource.title,
        "description": resource.description,
        "type": resource.resource_type,
        "url": resource.url,
        "imageUrl": resource.image_url,
        "source": resource.source,
        "featured": resource.featured,
    }


def _discussion_payload(discussion):
    return {
        "id": discussion.id,
        "title": discussion.title,
        "body": discussion.body,
        "author": discussion.author,
        "topic": discussion.topic,
        "replies": discussion.replies,
        "lastActivity": discussion.last_activity.isoformat(),
    }


def health(request):
    return JsonResponse({"status": "ok"})


def overview(request):
    prompt_count = PromptActivity.objects.count()
    curated_count = PromptActivity.objects.filter(status="curated").count()
    resource_count = Resource.objects.count()
    discussion_count = Discussion.objects.count()
    total_replies = Discussion.objects.aggregate(total=Sum("replies"))["total"] or 0

    subjects = (
        PromptActivity.objects.values("subject")
        .annotate(count=Count("id"))
        .order_by("-count", "subject")
    )

    return JsonResponse(
        {
            "metrics": {
                "prompts": prompt_count,
                "curated": curated_count,
                "resources": resource_count,
                "communityThreads": discussion_count,
                "communityReplies": total_replies,
            },
            "subjects": list(subjects),
            "latestPrompts": [
                _prompt_payload(prompt) for prompt in PromptActivity.objects.all()[:3]
            ],
            "featuredResources": [
                _resource_payload(resource)
                for resource in Resource.objects.filter(featured=True)[:3]
            ],
        }
    )


@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def prompts(request):
    if request.method == "POST":
        payload = json.loads(request.body or "{}")
        prompt = PromptActivity.objects.create(
            title=payload.get("title", "").strip(),
            summary=payload.get("summary", "").strip(),
            prompt=payload.get("prompt", "").strip(),
            subject=payload.get("subject", "General").strip(),
            level=payload.get("level", "Docentes").strip(),
            author=payload.get("author", "Docente invitado").strip(),
            tags=", ".join(payload.get("tags", [])),
            status="review",
        )
        return JsonResponse(_prompt_payload(prompt), status=201)

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    queryset = PromptActivity.objects.all()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(subject__icontains=query)
            | Q(tags__icontains=query)
        )
    if status:
        queryset = queryset.filter(status=status)

    return JsonResponse({"results": [_prompt_payload(prompt) for prompt in queryset]})


def resources(request):
    resource_type = request.GET.get("type", "").strip()
    queryset = Resource.objects.all()
    if resource_type:
        queryset = queryset.filter(resource_type=resource_type)
    return JsonResponse({"results": [_resource_payload(resource) for resource in queryset]})


def discussions(request):
    topic = request.GET.get("topic", "").strip()
    queryset = Discussion.objects.all()
    if topic:
        queryset = queryset.filter(topic=topic)
    return JsonResponse({"results": [_discussion_payload(item) for item in queryset]})
