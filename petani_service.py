from sqlalchemy.exc import SQLAlchemyError
from app.models.pertanian_models import db

class PetaniService:
    def __init__(self, repo):
        self.repo = repo

    def list_petani(self, search=''):
        items = self.repo.get_all(search)
        return [item.to_dict() for item in items]

    def detail_petani(self, petani_id):
        petani = self.repo.get_by_id(petani_id)
        if not petani:
            return None, "Data petani tidak ditemukan", 404
        return petani.to_dict(), None, 200

    def tambah_petani(self, data):
        if not data:
            return None, {"payload": "Body JSON wajib diisi"}, 400
        errors = {}
        if not data.get('nama_petani'):
            errors['nama_petani'] = "Nama petani wajib diisi"
        if not data.get('no_hp'):
            errors['no_hp'] = "Nomor HP wajib diisi"
        if not data.get('alamat'):
            errors['alamat'] = "Alamat wajib diisi"
        if errors:
            return None, errors, 400

        try:
            baru = self.repo.create(data['nama_petani'], data['no_hp'], data['alamat'])
            return baru.to_dict(), "Data petani berhasil ditambahkan", 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Gagal menyimpan data petani: {str(e)}", 500

    def ubah_petani(self, petani_id, data):
        petani = self.repo.get_by_id(petani_id)
        if not petani:
            return None, "Data petani tidak ditemukan", 404
        if not data:
            return None, {"payload": "Body JSON wajib diisi"}, 400
        try:
            updated = self.repo.update(petani, data)
            return updated.to_dict(), "Data petani berhasil diperbarui", 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Gagal memperbarui data: {str(e)}", 500

    def hapus_petani(self, petani_id):
        petani = self.repo.get_by_id(petani_id)
        if not petani:
            return "Data petani tidak ditemukan", 404
        try:
            self.repo.delete(petani)
            return "Data petani berhasil dihapus", 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"Gagal menghapus data: {str(e)}", 500
