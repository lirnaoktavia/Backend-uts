from flask import Blueprint, request
from app.repositories.lahan_repo import LahanRepository
from app.services.lahan_service import LahanService
from app.utils.response_helper import success_response, fail_response, error_response

lahan_bp = Blueprint('lahan', __name__, url_prefix='/api/v1/lahan')
service = LahanService(LahanRepository())

@lahan_bp.route('', methods=['GET'])
def get_all_lahan():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search = request.args.get('search', '', type=str)
    data, meta = service.list_lahan(page, per_page, search)
    return success_response(data=data, pagination=meta)

@lahan_bp.route('/<int:lahan_id>', methods=['GET'])
def get_lahan_by_id(lahan_id):
    data, err, code = service.detail_lahan(lahan_id)
    if code == 404:
        return fail_response({"id": err}, 404)
    return success_response(data=data)

@lahan_bp.route('', methods=['POST'])
def create_lahan():
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)
    data, msg_or_err, code = service.tambah_lahan(request.get_json())
    if code in (400, 404):
        return fail_response(msg_or_err, code)
    if code == 500:
        return error_response(msg_or_err, 500)
    return success_response(data=data, message=msg_or_err, code=201)

@lahan_bp.route('/transaksi-lengkap', methods=['POST'])
def create_lahan_transaksi_atomik():
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)
    data, msg_or_err, code = service.transaksi_lahan_lengkap(request.get_json())
    if code == 400:
        return fail_response(msg_or_err, 400)
    if code == 500:
        return error_response(msg_or_err, 500)
    return success_response(data=data, message=msg_or_err, code=201)

@lahan_bp.route('/<int:lahan_id>', methods=['PUT'])
def update_lahan(lahan_id):
    if not request.is_json:
        return fail_response({"content_type": "Header harus application/json"}, 400)
    data, msg_or_err, code = service.ubah_lahan(lahan_id, request.get_json())
    if code == 404:
        return fail_response({"id": msg_or_err}, 404)
    if code == 500:
        return error_response(msg_or_err, 500)
    return success_response(data=data, message=msg_or_err, code=200)

@lahan_bp.route('/<int:lahan_id>', methods=['DELETE'])
def delete_lahan(lahan_id):
    msg, code = service.hapus_lahan(lahan_id)
    if code == 404:
        return fail_response({"id": msg}, 404)
    if code == 500:
        return error_response(msg, 500)
    return success_response(message=msg, code=200)
