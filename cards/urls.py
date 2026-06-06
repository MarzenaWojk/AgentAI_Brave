from django.urls import path

from .views import (
    auth_login,
    auth_logout,
    auth_me,
    auth_register,
    flashcard_detail,
    flashcards_collection,
)

urlpatterns = [
    path("auth/register/", auth_register, name="auth-register"),
    path("auth/login/", auth_login, name="auth-login"),
    path("auth/logout/", auth_logout, name="auth-logout"),
    path("auth/me/", auth_me, name="auth-me"),
    path("flashcards/", flashcards_collection, name="flashcards-collection"),
    path("flashcards/<int:flashcard_id>/", flashcard_detail, name="flashcard-detail"),
]
