import json

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Flashcard


User = get_user_model()


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


def homepage(request):
	return JsonResponse(
		{
			"status": "ok",
			"message": "tenx_cards is running",
			"endpoints": {
				"health": "/health/",
				"flashcards": "/api/cards/flashcards/",
			},
		}
	)


def healthcheck(request):
	return JsonResponse({"status": "ok"})


def _parse_json_payload(request):
	try:
		return json.loads(request.body or "{}"), None
	except json.JSONDecodeError:
		return None, _error_response(
			code="INVALID_JSON",
			message="Request body must be valid JSON.",
			context={},
			status=400,
		)


@csrf_exempt
def auth_register(request):
	if request.method != "POST":
		return _error_response(
			code="METHOD_NOT_ALLOWED",
			message="Only POST is supported.",
			context={"method": request.method},
			status=405,
		)

	payload, error = _parse_json_payload(request)
	if error:
		return error

	username = payload.get("username")
	password = payload.get("password")

	missing_fields = [
		field
		for field, value in {"username": username, "password": password}.items()
		if not isinstance(value, str) or not value.strip()
	]
	if missing_fields:
		return _error_response(
			code="VALIDATION_ERROR",
			message="Both 'username' and 'password' are required non-empty strings.",
			context={"fields": missing_fields},
			status=400,
		)

	clean_username = username.strip()
	if User.objects.filter(username=clean_username).exists():
		return _error_response(
			code="VALIDATION_ERROR",
			message="Username already exists.",
			context={"fields": ["username"]},
			status=400,
		)

	user = User.objects.create_user(username=clean_username, password=password)
	login(request, user)

	return JsonResponse(
		{"data": {"id": user.id, "username": user.get_username()}},
		status=201,
	)


@csrf_exempt
def auth_login(request):
	if request.method != "POST":
		return _error_response(
			code="METHOD_NOT_ALLOWED",
			message="Only POST is supported.",
			context={"method": request.method},
			status=405,
		)

	payload, error = _parse_json_payload(request)
	if error:
		return error

	username = payload.get("username")
	password = payload.get("password")

	missing_fields = [
		field
		for field, value in {"username": username, "password": password}.items()
		if not isinstance(value, str) or not value.strip()
	]
	if missing_fields:
		return _error_response(
			code="VALIDATION_ERROR",
			message="Both 'username' and 'password' are required non-empty strings.",
			context={"fields": missing_fields},
			status=400,
		)

	user = authenticate(
		request,
		username=username.strip(),
		password=password,
	)
	if user is None:
		return _error_response(
			code="INVALID_CREDENTIALS",
			message="Invalid username or password.",
			context={},
			status=401,
		)

	login(request, user)
	return JsonResponse({"data": {"id": user.id, "username": user.get_username()}})


@csrf_exempt
def auth_logout(request):
	if request.method != "POST":
		return _error_response(
			code="METHOD_NOT_ALLOWED",
			message="Only POST is supported.",
			context={"method": request.method},
			status=405,
		)

	if not request.user.is_authenticated:
		return _error_response(
			code="AUTH_REQUIRED",
			message="Authentication required.",
			context={},
			status=401,
		)

	logout(request)
	return JsonResponse({}, status=200)


def auth_me(request):
	if request.method != "GET":
		return _error_response(
			code="METHOD_NOT_ALLOWED",
			message="Only GET is supported.",
			context={"method": request.method},
			status=405,
		)

	if not request.user.is_authenticated:
		return _error_response(
			code="AUTH_REQUIRED",
			message="Authentication required.",
			context={},
			status=401,
		)

	return JsonResponse(
		{"data": {"id": request.user.id, "username": request.user.get_username()}}
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

	payload, error = _parse_json_payload(request)
	if error:
		return error

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
	if request.method == "DELETE":
		try:
			flashcard = Flashcard.objects.get(id=flashcard_id)
		except Flashcard.DoesNotExist:
			return _error_response(
				code="NOT_FOUND",
				message="Flashcard was not found.",
				context={"id": flashcard_id},
				status=404,
			)

		flashcard.delete()
		return JsonResponse({}, status=204)

	if request.method != "GET":
		return _error_response(
			code="METHOD_NOT_ALLOWED",
			message="Only GET and DELETE are supported for this endpoint.",
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
