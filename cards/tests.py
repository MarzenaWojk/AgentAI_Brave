import json

from django.test import Client, TestCase


class FlashcardsApiTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_invalid_json_returns_structured_error(self):
		response = self.client.post(
			"/api/cards/flashcards/",
			data="{invalid",
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()["error"]["code"], "INVALID_JSON")
		self.assertIn("message", response.json()["error"])
		self.assertIn("context", response.json()["error"])

	def test_validation_error_returns_structured_error(self):
		response = self.client.post(
			"/api/cards/flashcards/",
			data=json.dumps({"front": "Hello"}),
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()["error"]["code"], "VALIDATION_ERROR")
		self.assertEqual(response.json()["error"]["context"]["fields"], ["back"])

	def test_not_found_returns_structured_error(self):
		response = self.client.get("/api/cards/flashcards/999/")

		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.json()["error"]["code"], "NOT_FOUND")
		self.assertEqual(response.json()["error"]["context"]["id"], 999)

	def test_method_not_allowed_returns_structured_error(self):
		response = self.client.put("/api/cards/flashcards/1/")

		self.assertEqual(response.status_code, 405)
		self.assertEqual(response.json()["error"]["code"], "METHOD_NOT_ALLOWED")

	def test_create_flashcard_success(self):
		response = self.client.post(
			"/api/cards/flashcards/",
			data=json.dumps({"front": "Q", "back": "A"}),
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 201)
		self.assertIn("data", response.json())
		self.assertEqual(response.json()["data"]["front"], "Q")
		self.assertEqual(response.json()["data"]["back"], "A")

	def test_delete_flashcard_success(self):
		response = self.client.post(
			"/api/cards/flashcards/",
			data=json.dumps({"front": "Q", "back": "A"}),
			content_type="application/json",
		)
		flashcard_id = response.json()["data"]["id"]

		response = self.client.delete(f"/api/cards/flashcards/{flashcard_id}/")

		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.content, b"")

		response = self.client.get(f"/api/cards/flashcards/{flashcard_id}/")
		self.assertEqual(response.status_code, 404)

	def test_delete_nonexistent_flashcard(self):
		response = self.client.delete("/api/cards/flashcards/999/")

		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.json()["error"]["code"], "NOT_FOUND")
		self.assertEqual(response.json()["error"]["context"]["id"], 999)
