from app.models.pertanian_models import db, Petani

class PetaniRepository:
    def get_all(self, search=''):
        query = Petani.query
        if search:
            query = query.filter(Petani.nama_petani.ilike(f"%{search}%"))
        return query.all()

    def get_by_id(self, petani_id):
        return db.session.get(Petani, petani_id)

    def create(self, nama_petani, no_hp, alamat):
        petani_baru = Petani(nama_petani=nama_petani, no_hp=no_hp, alamat=alamat)
        db.session.add(petani_baru)
        db.session.commit()
        return petani_baru

    def update(self, petani, data):
        petani.nama_petani = data.get('nama_petani', petani.nama_petani)
        petani.no_hp = data.get('no_hp', petani.no_hp)
        petani.alamat = data.get('alamat', petani.alamat)
        db.session.commit()
        return petani

    def delete(self, petani):
        db.session.delete(petani)
        db.session.commit()
