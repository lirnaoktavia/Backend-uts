from sqlalchemy.exc import SQLAlchemyError
from app.models.pertanian_models import db, Lahan

class TanamanService:
    def __init__(self, repo):
        self.repo = repo

    def list_tanaman(self, page=1, per_page=5, search='', lahan_id=None):
        paginated = self.repo.get_paginated(page, per_page, search, lahan_id)
        data = [item.to_dict() for item in paginated.items]
        meta = {
            "current_page": paginated.page,
            "per_page": paginated.per_page,
            "total_pages": paginated.pages,
            "total_items": paginated.total
        }
        return data, meta

    def detail_tanaman(self, tanaman_id):
        tanaman = self.repo.get_by_id(tanaman_id)
        if not tanaman:
            return None, "Data tanaman tidak ditemukan", 404
        return tanaman.to_dict(), None, 200

    def tambah_tanaman(self, data):
        if not data:
            return None, {"payload": "Body JSON wajib diisi"}, 400
        errors = {}
        if not data.get('nama_tanaman'):
            errors['nama_tanaman'] = "Nama tanaman wajib diisi"
        if not data.get('varietas'):
            errors['varietas'] = "Varietas wajib diisi"
        if not data.get('tanggal_tanam'):
            errors['tanggal_tanam'] = "Tanggal tanam wajib diisi"
        if not data.get('lahan_id'):
            errors['lahan_id'] = "lahan_id wajib diisi"
        if errors:
            return None, errors, 400

        if not db.session.get(Lahan, data['lahan_id']):
            return None, {"lahan_id": "ID Lahan tidak ditemukan di database"}, 404

        try:
            baru = self.repo.create(
                data['nama_tanaman'],
                data['varietas'],
                data['tanggal_tanam'],
                data.get('status_tumbuh', 'Masa Tanam'),
                data['lahan_id']
            )
            return baru.to_dict(), "Data tanaman berhasil ditambahkan", 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Gagal menyimpan tanaman: {str(e)}", 500

    def ubah_tanaman(self, tanaman_id, data):
        tanaman = self.repo.get_by_id(tanaman_id)
        if not tanaman:
            return None, "Data tanaman tidak ditemukan", 404
        try:
            updated = self.repo.update(tanaman, data)
            return updated.to_dict(), "Data tanaman berhasil diperbarui", 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Gagal memperbarui tanaman: {str(e)}", 500

    def hapus_tanaman(self, tanaman_id):
        tanaman = self.repo.get_by_id(tanaman_id)
        if not tanaman:
            return "Data tanaman tidak ditemukan", 404
        try:
            self.repo.delete(tanaman)
            return "Data tanaman berhasil dihapus", 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"Gagal menghapus tanaman: {str(e)}", 500
