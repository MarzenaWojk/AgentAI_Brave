import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Flashcard


def _error_response(code, message, context, status):
	return JsonResponse(
		{
			"error": {
				"code": code,
				"message": message,
				"context": context,
			}
		},
		status=status,
	)


@csrf_exempt
def flashcards_collection(request):
	if request.method == "GET":
		flashcards = Flashcard.objects.all().order_by("-created_at")
		return JsonResponse(
			{
				"data": [
					{
						"id": flashcard.id,
						"front": flashcard.front,
						"back": flashcard.back,
						"created_at": flashcard.created_at.isoformat(),
					}
					for flashcard in flashcards
				]
			}
		)

	if request.method != "POST":
		return _error_response(
			code="METHOD_NOT_ALLOWED",
			message="Only GET and POST are supported.",
			context={"method": request.method},
			status=405,
		)

	try:
		payload = json.loads(request.body or "{}")
	except json.JSONDecodeError:
		return _error_response(
			code="INVALID_JSON",
			message="Request body must be valid JSON.",
			context={},
			status=400,
		)

	front = payload.get("front")
	back = payload.get("back")

	missing_fields = [
		field
		for field, value in {"front": front, "back": back}.items()
		if not isinstance(value, str) or not value.strip()
	]
	if missing_fields:
		return _error_response(
			code="VALIDATION_ERROR",
			message="Both 'front' and 'back' are required non-empty strings.",
			context={"fields": missing_fields},
			status=400,
		)

	flashcard = Flashcard.objects.create(front=front.strip(), back=back.strip())
	return JsonResponse(
		{
			"data": {
				"id": flashcard.id,
				"front": flashcard.front,
				"back": flashcard.back,
				"created_at": flashcard.created_at.isoformat(),
			}
		},
		status=201,
	)


def flashcard_detail(request, flashcard_id):
	if request.method != "GET":
		return _error_response(
			code="METHOD_NOT_ALLOWED",
			message="Only GET is supported for this endpoint.",
			context={"method": request.method},
			status=405,
		)

	try:
		flashcard = Flashcard.objects.get(id=flashcard_id)
	except Flashcard.DoesNotExist:
		return _error_response(
			code="NOT_FOUND",
			message="Flashcard was not found.",
			context={"id": flashcard_id},
			status=404,
		)

	return JsonResponse(
		{
			"data": {
				"id": flashcard.id,
				"front": flashcard.front,
				"back": flashcard.back,
				"created_at": flashcard.created_at.isoformat(),
			}
		}
	)
