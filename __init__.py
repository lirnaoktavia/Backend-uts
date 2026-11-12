from flask import Flask
from app.config import Config
from app.models.pertanian_models import db, Petani, Lahan, Tanaman
from app.routes.petani_routes import petani_bp
from app.routes.lahan_routes import lahan_bp
from app.routes.tanaman_routes import tanaman_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Registrasi Blueprint RESTful API
    app.register_blueprint(petani_bp)
    app.register_blueprint(lahan_bp)
    app.register_blueprint(tanaman_bp)

    # Membuat otomatis 3 tabel berelasi di MySQL
    with app.app_context():
        db.create_all()

    return app
