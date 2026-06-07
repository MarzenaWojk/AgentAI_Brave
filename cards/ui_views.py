from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import Flashcard


def home_page(request):
	if request.user.is_authenticated:
		return redirect("dashboard")
	return render(request, "cards/home.html")


@require_http_methods(["GET", "POST"])
def register_page(request):
	if request.user.is_authenticated:
		return redirect("dashboard")

	form = UserCreationForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		user = form.save()
		login(request, user)
		messages.success(request, "Your account has been created.")
		return redirect("dashboard")

	return render(request, "cards/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_page(request):
	if request.user.is_authenticated:
		return redirect("dashboard")

	form = AuthenticationForm(request, data=request.POST or None)
	if request.method == "POST" and form.is_valid():
		login(request, form.get_user())
		messages.success(request, "Welcome back.")
		return redirect("dashboard")

	return render(request, "cards/login.html", {"form": form})


@require_http_methods(["POST"])
def logout_page(request):
	if request.user.is_authenticated:
		logout(request)
	messages.info(request, "You have been logged out.")
	return redirect("login")


@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def dashboard_page(request):
	front_value = ""
	back_value = ""

	if request.method == "POST":
		action = request.POST.get("action")

		if action == "create":
			front_value = (request.POST.get("front") or "").strip()
			back_value = (request.POST.get("back") or "").strip()

			missing_fields = []
			if not front_value:
				missing_fields.append("front")
			if not back_value:
				missing_fields.append("back")

			if missing_fields:
				messages.error(
					request,
					"Both front and back are required.",
				)
			else:
				Flashcard.objects.create(
					owner=request.user,
					front=front_value,
					back=back_value,
				)
				messages.success(request, "Flashcard created.")
				return redirect("dashboard")

		elif action == "delete":
			flashcard_id = request.POST.get("flashcard_id")
			deleted, _ = Flashcard.objects.filter(
				id=flashcard_id,
				owner=request.user,
			).delete()
			if deleted:
				messages.success(request, "Flashcard deleted.")
			else:
				messages.error(request, "Flashcard not found.")
			return redirect("dashboard")

	flashcards = Flashcard.objects.filter(owner=request.user).order_by("-created_at")
	return render(
		request,
		"cards/dashboard.html",
		{
			"flashcards": flashcards,
			"front_value": front_value,
			"back_value": back_value,
		},
	)
