import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class FlashcardsApiTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user_model = get_user_model()

	def test_auth_register_returns_user_data_and_creates_session(self):
		register_response = self.client.post(
			"/api/cards/auth/register/",
			data=json.dumps({"username": "anna", "password": "StrongPass123"}),
			content_type="application/json",
		)

		self.assertEqual(register_response.status_code, 201)
		self.assertEqual(register_response.json()["data"]["username"], "anna")

		me_response = self.client.get("/api/cards/auth/me/")
		self.assertEqual(me_response.status_code, 200)
		self.assertEqual(me_response.json()["data"]["username"], "anna")

	def test_auth_login_returns_user_data_and_creates_session(self):
		self.user_model.objects.create_user(username="ola", password="StrongPass123")

		login_response = self.client.post(
			"/api/cards/auth/login/",
			data=json.dumps({"username": "ola", "password": "StrongPass123"}),
			content_type="application/json",
		)

		self.assertEqual(login_response.status_code, 200)
		self.assertEqual(login_response.json()["data"]["username"], "ola")

		me_response = self.client.get("/api/cards/auth/me/")
		self.assertEqual(me_response.status_code, 200)
		self.assertEqual(me_response.json()["data"]["username"], "ola")

	def test_auth_me_requires_session(self):
		response = self.client.get("/api/cards/auth/me/")

		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.json()["error"]["code"], "AUTH_REQUIRED")

	def test_homepage_returns_status_payload(self):
		response = self.client.get("/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()["status"], "ok")
		self.assertEqual(response.json()["endpoints"]["health"], "/health/")

	def test_healthcheck_returns_ok(self):
		response = self.client.get("/health/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {"status": "ok"})

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
