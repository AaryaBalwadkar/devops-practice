import json
import unittest
from app import app

class PaymentApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_payment_creates_notification(self):
        response = self.client.post(
            "/api/payments",
            data=json.dumps({"customer": "Exam User", "amount": 125.50}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(body["payment"]["status"], "SUCCESS")
        self.assertEqual(body["notification"]["status"], "RECORDED")

    def test_rejects_invalid_amount(self):
        response = self.client.post(
            "/api/payments",
            json={"customer": "Exam User", "amount": -10},
        )
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
