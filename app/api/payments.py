from flask import Blueprint, request, jsonify
from app.services import PaymentService

payments_bp = Blueprint("payments", __name__)
payment_service = PaymentService()

@payments_bp.route("/", methods=["GET"])
def get_all_payments():
    payments = payment_service.get_all_payments()
    return jsonify([p.to_dict() for p in payments])

@payments_bp.route("/<int:payment_id>", methods=["GET"])
def get_payment(payment_id):
    payment = payment_service.get_payment_by_id(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(payment.to_dict())

@payments_bp.route("/", methods=["POST"])
def create_payment():
    data = request.json
    new_payment = payment_service.create_payment(data)
    return jsonify(new_payment.to_dict()), 201

@payments_bp.route("/<int:payment_id>", methods=["PUT"])
def update_payment(payment_id):
    data = request.json
    updated_payment = payment_service.update_payment(payment_id, data)
    if not updated_payment:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(updated_payment.to_dict())

@payments_bp.route("/<int:payment_id>", methods=["DELETE"])
def delete_payment(payment_id):
    success = payment_service.delete_payment(payment_id)
    if not success:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify({"message": "Payment deleted"})