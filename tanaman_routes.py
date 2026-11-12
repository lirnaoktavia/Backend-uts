from flask import Blueprint, request
from app.repositories.tanaman_repo import TanamanRepository
from app.services.tanaman_service import TanamanService
from app.utils.response_helper import success_response, fail_response, error_response

tanaman_bp = Blueprint('tanaman', __name__, url_prefix='/api/v1/tanaman')
service = TanamanService(TanamanRepository())

@tanaman_bp.route('', methods=['GET'])
def get_all_tanaman():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search = request.args.get('search', '', type=str)
    lahan_id = request.args.get('lahan_id', None, type=int)
    data, meta = service.list_tanaman(page, per_page, search, lahan_id)
    return success_response(data=data, pagination=meta)

@tanaman_bp.route('/<int:tanaman_id>', methods=['GET'])
def get_tanaman_by_id(tanaman_id):
    data, err, code = service.detail_tanaman(tanaman_id)
    if code == 404:
        return fail_response({"id": err}, 404)
    return success_response(data=data)

@tanaman_bp.route('', methods=['POST'])
def create_tanaman():
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)
    data, msg_or_err, code = service.tambah_tanaman(request.get_json())
    if code in (400, 404):
        return fail_response(msg_or_err, code)
    if code == 500:
        return error_response(msg_or_err, 500)
    return success_response(data=data, message=msg_or_err, code=201)

@tanaman_bp.route('/<int:tanaman_id>', methods=['PUT'])
def update_tanaman(tanaman_id):
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)
    data, msg_or_err, code = service.ubah_tanaman(tanaman_id, request.get_json())
    if code == 404:
        return fail_response({"id": msg_or_err}, 404)
    if code == 500:
        return error_response(msg_or_err, 500)
    return success_response(data=data, message=msg_or_err, code=200)

@tanaman_bp.route('/<int:tanaman_id>', methods=['DELETE'])
def delete_tanaman(tanaman_id):
    msg, code = service.hapus_tanaman(tanaman_id)
    if code == 404:
        return fail_response({"id": msg}, 404)
    if code == 500:
        return error_response(msg, 500)
    return success_response(message=msg, code=200)
