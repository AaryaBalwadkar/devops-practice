from flask import Flask, jsonify, request
from datetime import datetime, timezone
from uuid import uuid4

app = Flask(__name__)
payments = []
notifications = []

@app.get("/")
def root():
    return jsonify({
        "service": "MiniPay Payment API",
        "message": "Use POST /api/payments to simulate a payment.",
        "health": "/api/health"
    })

@app.get("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "payment-backend"}), 200

@app.post("/api/payments")
def create_payment():
    data = request.get_json(silent=True) or {}
    customer = str(data.get("customer", "")).strip()
    amount = data.get("amount")

    if not customer:
        return jsonify({"error": "customer is required"}), 400
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "amount must be a positive number"}), 400

    payment = {
        "payment_id": "pay_" + uuid4().hex[:10],
        "customer": customer,
        "amount": round(float(amount), 2),
        "currency": "INR",
        "status": "SUCCESS",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    payments.append(payment)
    notifications.append({
        "notification_id": "ntf_" + uuid4().hex[:10],
        "payment_id": payment["payment_id"],
        "message": f"Payment of INR {payment['amount']:.2f} was simulated successfully.",
        "channel": "console-log",
        "status": "RECORDED",
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    app.logger.info("Payment simulated: %s; notification recorded", payment["payment_id"])
    return jsonify({"payment": payment, "notification": notifications[-1]}), 201

@app.get("/api/payments")
def list_payments():
    return jsonify({"count": len(payments), "payments": payments}), 200

@app.get("/api/notifications")
def list_notifications():
    return jsonify({"count": len(notifications), "notifications": notifications}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
