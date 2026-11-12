from flask import Blueprint, request
from app.repositories.petani_repo import PetaniRepository
from app.services.petani_service import PetaniService
from app.utils.response_helper import success_response, fail_response, error_response

petani_bp = Blueprint('petani', __name__, url_prefix='/api/v1/petani')
service = PetaniService(PetaniRepository())

@petani_bp.route('', methods=['GET'])
def get_all_petani():
    search = request.args.get('search', '', type=str)
    data = service.list_petani(search)
    return success_response(data=data)

@petani_bp.route('/<int:petani_id>', methods=['GET'])
def get_petani_by_id(petani_id):
    data, err, code = service.detail_petani(petani_id)
    if code == 404:
        return fail_response({"id": err}, 404)
    return success_response(data=data)

@petani_bp.route('', methods=['POST'])
def create_petani():
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)
    data, msg_or_err, code = service.tambah_petani(request.get_json())
    if code == 400:
        return fail_response(msg_or_err, 400)
    if code == 500:
        return error_response(msg_or_err, 500)
    return success_response(data=data, message=msg_or_err, code=201)

@petani_bp.route('/<int:petani_id>', methods=['PUT'])
def update_petani(petani_id):
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)
    data, msg_or_err, code = service.ubah_petani(petani_id, request.get_json())
    if code in (400, 404):
        return fail_response({"detail": msg_or_err}, code)
    if code == 500:
        return error_response(msg_or_err, 500)
    return success_response(data=data, message=msg_or_err, code=200)

@petani_bp.route('/<int:petani_id>', methods=['DELETE'])
def delete_petani(petani_id):
    msg, code = service.hapus_petani(petani_id)
    if code == 404:
        return fail_response({"id": msg}, 404)
    if code == 500:
        return error_response(msg, 500)
    return success_response(message=msg, code=200)
