from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# TABEL 1: PETANI (Induk dari Lahan - Relasi 1:N)
class Petani(db.Model):
    __tablename__ = 'petani'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_petani = db.Column(db.String(100), nullable=False)
    no_hp = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)

    daftar_lahan = db.relationship('Lahan', backref='petani', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nama_petani": self.nama_petani,
            "no_hp": self.no_hp,
            "alamat": self.alamat,
            "jumlah_lahan": len(self.daftar_lahan)
        }

# TABEL 2: LAHAN (Anak dari Petani & Induk dari Tanaman - Relasi 1:N)
class Lahan(db.Model):
    __tablename__ = 'lahan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_lahan = db.Column(db.String(100), nullable=False)
    lokasi = db.Column(db.String(150), nullable=False)
    luas_hektar = db.Column(db.Float, nullable=False)
    petani_id = db.Column(db.Integer, db.ForeignKey('petani.id'), nullable=False)

    daftar_tanaman = db.relationship('Tanaman', backref='lahan', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nama_lahan": self.nama_lahan,
            "lokasi": self.lokasi,
            "luas_hektar": self.luas_hektar,
            "petani_id": self.petani_id,
            "pemilik": self.petani.nama_petani if self.petani else None,
            "jumlah_tanaman": len(self.daftar_tanaman)
        }

# TABEL 3: TANAMAN (Anak dari Lahan)
class Tanaman(db.Model):
    __tablename__ = 'tanaman'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_tanaman = db.Column(db.String(100), nullable=False)
    varietas = db.Column(db.String(100), nullable=False)
    tanggal_tanam = db.Column(db.String(20), nullable=False)
    status_tumbuh = db.Column(db.String(50), default="Masa Tanam", nullable=False)
    lahan_id = db.Column(db.Integer, db.ForeignKey('lahan.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nama_tanaman": self.nama_tanaman,
            "varietas": self.varietas,
            "tanggal_tanam": self.tanggal_tanam,
            "status_tumbuh": self.status_tumbuh,
            "lahan_id": self.lahan_id,
            "nama_lahan": self.lahan.nama_lahan if self.lahan else None,
            "pemilik_lahan": self.lahan.petani.nama_petani if (self.lahan and self.lahan.petani) else None
        }
