from flask import Blueprint, request
from app.services.payment_service import PaymentService
from app.utils.responses import json_response

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('', methods=['GET'])
def get_payments():
    try:
        payments = PaymentService.get_all_payments()
        return json_response(data=[p.to_dict() for p in payments])
    except Exception as e:
        return json_response(message="Internal server error", status=500)

@payments_bp.route('', methods=['POST'])
def add_payment():
    try:
        data = request.get_json()
        payment = PaymentService.create_payment(data)
        return json_response(data=payment.to_dict(), status=201)
    except ValueError as e:
        return json_response(message=str(e), status=400)
    except Exception as e:
        return json_response(message="Internal server error", status=500)