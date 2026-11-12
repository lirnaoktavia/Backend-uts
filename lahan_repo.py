from app.models.pertanian_models import db, Petani, Lahan, Tanaman

class LahanRepository:
    def get_paginated(self, page=1, per_page=5, search=''):
        query = Lahan.query
        if search:
            query = query.filter(Lahan.nama_lahan.ilike(f"%{search}%"))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    def get_by_id(self, lahan_id):
        return db.session.get(Lahan, lahan_id)

    def create(self, nama_lahan, lokasi, luas_hektar, petani_id):
        lahan_baru = Lahan(
            nama_lahan=nama_lahan,
            lokasi=lokasi,
            luas_hektar=luas_hektar,
            petani_id=petani_id
        )
        db.session.add(lahan_baru)
        db.session.commit()
        return lahan_baru

    def create_transaksi_atomik(self, data):
        petani = Petani.query.filter_by(nama_petani=data['nama_petani']).first()
        if not petani:
            petani = Petani(
                nama_petani=data['nama_petani'],
                no_hp=data.get('no_hp', '-'),
                alamat=data.get('alamat', '-')
            )
            db.session.add(petani)
            db.session.flush()

        lahan = Lahan(
            nama_lahan=data['nama_lahan'],
            lokasi=data['lokasi'],
            luas_hektar=float(data['luas_hektar']),
            petani_id=petani.id
        )
        db.session.add(lahan)
        db.session.flush()

        tanaman = Tanaman(
            nama_tanaman=data['nama_tanaman'],
            varietas=data.get('varietas', 'Unggul'),
            tanggal_tanam=data['tanggal_tanam'],
            status_tumbuh=data.get('status_tumbuh', 'Masa Tanam'),
            lahan_id=lahan.id
        )
        db.session.add(tanaman)
        db.session.commit()
        return lahan

    def update(self, lahan, data):
        lahan.nama_lahan = data.get('nama_lahan', lahan.nama_lahan)
        lahan.lokasi = data.get('lokasi', lahan.lokasi)
        if 'luas_hektar' in data:
            lahan.luas_hektar = float(data['luas_hektar'])
        db.session.commit()
        return lahan

    def delete(self, lahan):
        db.session.delete(lahan)
        db.session.commit()
