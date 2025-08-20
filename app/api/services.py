from flask import Blueprint, request, jsonify
from app.services.service_service import ServiceService

services_bp = Blueprint("services", __name__)
service_service = ServiceService()

@services_bp.route("/", methods=["GET"])
def get_all_services():
    services = service_service.get_all_services()
    return jsonify([s.to_dict() for s in services])

@services_bp.route("/<int:service_id>", methods=["GET"])
def get_service(service_id):
    service = service_service.get_service_by_id(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    return jsonify(service.to_dict())

@services_bp.route("/", methods=["POST"])
def create_service():
    data = request.json
    new_service = service_service.create_service(data)
    return jsonify(new_service.to_dict()), 201

@services_bp.route("/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    data = request.json
    updated_service = service_service.update_service(service_id, data)
    if not updated_service:
        return jsonify({"error": "Service not found"}), 404
    return jsonify(updated_service.to_dict())

@services_bp.route("/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    success = service_service.delete_service(service_id)
    if not success:
        return jsonify({"error": "Service not found"}), 404
    return jsonify({"message": "Service deleted"})
