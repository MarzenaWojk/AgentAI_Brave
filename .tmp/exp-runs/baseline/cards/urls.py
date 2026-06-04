from django.urls import path

from .views import flashcard_detail, flashcards_collection

urlpatterns = [
    path("flashcards/", flashcards_collection, name="flashcards-collection"),
    path("flashcards/<int:flashcard_id>/", flashcard_detail, name="flashcard-detail"),
]
