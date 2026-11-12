from sqlalchemy.exc import SQLAlchemyError
from app.models.pertanian_models import db, Petani

class LahanService:
    def __init__(self, repo):
        self.repo = repo

    def list_lahan(self, page=1, per_page=5, search=''):
        paginated = self.repo.get_paginated(page, per_page, search)
        data = [item.to_dict() for item in paginated.items]
        meta = {
            "current_page": paginated.page,
            "per_page": paginated.per_page,
            "total_pages": paginated.pages,
            "total_items": paginated.total
        }
        return data, meta

    def detail_lahan(self, lahan_id):
        lahan = self.repo.get_by_id(lahan_id)
        if not lahan:
            return None, "Data lahan tidak ditemukan", 404
        detail = lahan.to_dict()
        detail["daftar_tanaman"] = [t.to_dict() for t in lahan.daftar_tanaman]
        return detail, None, 200

    def tambah_lahan(self, data):
        if not data:
            return None, {"payload": "Body JSON wajib diisi"}, 400
        errors = {}
        if not data.get('nama_lahan'):
            errors['nama_lahan'] = "Nama lahan wajib diisi"
        if not data.get('lokasi'):
            errors['lokasi'] = "Lokasi lahan wajib diisi"
        if data.get('luas_hektar') is None:
            errors['luas_hektar'] = "Luas hektar wajib diisi"
        if not data.get('petani_id'):
            errors['petani_id'] = "petani_id wajib diisi"
        if errors:
            return None, errors, 400

        if not db.session.get(Petani, data['petani_id']):
            return None, {"petani_id": "ID Petani tidak ditemukan di database"}, 404

        try:
            luas = float(data['luas_hektar'])
            if luas <= 0:
                return None, {"luas_hektar": "Luas lahan harus lebih dari 0"}, 400
            baru = self.repo.create(data['nama_lahan'], data['lokasi'], luas, data['petani_id'])
            return baru.to_dict(), "Data lahan berhasil ditambahkan", 201
        except (SQLAlchemyError, ValueError, TypeError) as e:
            db.session.rollback()
            return None, f"Transaksi gagal dan di-rollback: {str(e)}", 500

    def transaksi_lahan_lengkap(self, data):
        if not data:
            return None, {"payload": "Body JSON wajib diisi"}, 400
        wajib = ['nama_petani', 'nama_lahan', 'lokasi', 'luas_hektar', 'nama_tanaman', 'tanggal_tanam']
        errors = {field: f"Field '{field}' wajib diisi" for field in wajib if not data.get(field)}
        if errors:
            return None, errors, 400

        try:
            if float(data['luas_hektar']) <= 0:
                return None, {"luas_hektar": "Luas hektar harus lebih dari 0"}, 400
            lahan_baru = self.repo.create_transaksi_atomik(data)
            return lahan_baru.to_dict(), "Transaksi atomik Petani, Lahan, dan Tanaman berhasil disimpan", 201
        except (SQLAlchemyError, ValueError, TypeError) as e:
            db.session.rollback()
            return None, f"Transaksi atomik dibatalkan (Rollback): {str(e)}", 500

    def ubah_lahan(self, lahan_id, data):
        lahan = self.repo.get_by_id(lahan_id)
        if not lahan:
            return None, "Data lahan tidak ditemukan", 404
        try:
            updated = self.repo.update(lahan, data)
            return updated.to_dict(), "Data lahan berhasil diperbarui", 200
        except (SQLAlchemyError, ValueError, TypeError) as e:
            db.session.rollback()
            return None, f"Gagal memperbarui lahan: {str(e)}", 500

    def hapus_lahan(self, lahan_id):
        lahan = self.repo.get_by_id(lahan_id)
        if not lahan:
            return "Data lahan tidak ditemukan", 404
        try:
            self.repo.delete(lahan)
            return "Data lahan berhasil dihapus", 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"Gagal menghapus lahan: {str(e)}", 500
