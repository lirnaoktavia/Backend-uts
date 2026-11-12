from app.models.pertanian_models import db, Tanaman

class TanamanRepository:
    def get_paginated(self, page=1, per_page=5, search='', lahan_id=None):
        query = Tanaman.query
        if lahan_id:
            query = query.filter_by(lahan_id=lahan_id)
        if search:
            query = query.filter(Tanaman.nama_tanaman.ilike(f"%{search}%"))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    def get_by_id(self, tanaman_id):
        return db.session.get(Tanaman, tanaman_id)

    def create(self, nama_tanaman, varietas, tanggal_tanam, status_tumbuh, lahan_id):
        tanaman_baru = Tanaman(
            nama_tanaman=nama_tanaman,
            varietas=varietas,
            tanggal_tanam=tanggal_tanam,
            status_tumbuh=status_tumbuh,
            lahan_id=lahan_id
        )
        db.session.add(tanaman_baru)
        db.session.commit()
        return tanaman_baru

    def update(self, tanaman, data):
        tanaman.nama_tanaman = data.get('nama_tanaman', tanaman.nama_tanaman)
        tanaman.varietas = data.get('varietas', tanaman.varietas)
        tanaman.tanggal_tanam = data.get('tanggal_tanam', tanaman.tanggal_tanam)
        tanaman.status_tumbuh = data.get('status_tumbuh', tanaman.status_tumbuh)
        db.session.commit()
        return tanaman

    def delete(self, tanaman):
        db.session.delete(tanaman)
        db.session.commit()
