from django.conf import settings
from django.db import models


class GenerationBatch(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="generation_batches")
	source_text = models.TextField(blank=True)
	requested_count = models.PositiveIntegerField(default=5)
	created_at = models.DateTimeField(auto_now_add=True)


class Flashcard(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="flashcards",
		null=True,
		blank=True,
	)
	generation_batch = models.ForeignKey(
		GenerationBatch,
		on_delete=models.CASCADE,
		related_name="flashcards",
		null=True,
		blank=True,
	)
	front = models.TextField()
	back = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
