# Sistem Manajemen Data Lahan dan Tanaman (RESTful API)

Proyek UTS Pemrograman Backend — STIKOM PGRI Banyuwangi (NIM Akhir Genap: 30).

## Arsitektur & Teknologi
- **Framework**: Python Flask
- **ORM & Database**: Flask-SQLAlchemy + PyMySQL (MySQL)
- **Arsitektur**: Layered Architecture (`models`, `repositories`, `services`, `routes`, `utils`)

## Cara Instalasi & Menjalankan
1. Buat database baru di MySQL bernama `db_lahan_tanaman`.
2. Buat dan aktifkan virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instal seluruh dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan server:
   ```bash
   python run.py
   ```
   Server berjalan di `http://127.0.0.1:5000`.

## Daftar Endpoint RESTful API

| Resource | Method | Endpoint | Keterangan |
| :--- | :--- | :--- | :--- |
| Petani | `GET` | `/api/v1/petani` | Ambil semua petani (`?search=`) |
| Petani | `GET` | `/api/v1/petani/<id>` | Detail petani |
| Petani | `POST` | `/api/v1/petani` | Tambah petani baru |
| Petani | `PUT` | `/api/v1/petani/<id>` | Ubah data petani |
| Petani | `DELETE` | `/api/v1/petani/<id>` | Hapus data petani |
| Lahan | `GET` | `/api/v1/lahan` | Ambil daftar lahan (`?page=&per_page=&search=`) |
| Lahan | `GET` | `/api/v1/lahan/<id>` | Detail lahan beserta daftar tanaman |
| Lahan | `POST` | `/api/v1/lahan` | Tambah lahan baru |
| Lahan | `POST` | `/api/v1/lahan/transaksi-lengkap` | Transaksi atomik 3 tabel + rollback |
| Lahan | `PUT` | `/api/v1/lahan/<id>` | Ubah data lahan |
| Lahan | `DELETE` | `/api/v1/lahan/<id>` | Hapus data lahan |
| Tanaman | `GET` | `/api/v1/tanaman` | Ambil daftar tanaman (`?page=&per_page=&search=&lahan_id=`) |
| Tanaman | `GET` | `/api/v1/tanaman/<id>` | Detail tanaman |
| Tanaman | `POST` | `/api/v1/tanaman` | Tambah tanaman baru |
| Tanaman | `PUT` | `/api/v1/tanaman/<id>` | Ubah data/status tanaman |
| Tanaman | `DELETE` | `/api/v1/tanaman/<id>` | Hapus data tanaman |
