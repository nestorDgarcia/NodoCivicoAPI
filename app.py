from flask import Flask
from flask_cors import CORS
from config import Config
from models import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = Config.DEBUG

    CORS(app)
    db.init_app(app)

    # Registrar blueprints
    from routes.reports import reports_bp
    from routes.categories import categories_bp
    from routes.users import users_bp

    app.register_blueprint(reports_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(users_bp)

    # Crear tablas y poblar datos iniciales
    with app.app_context():
        db.create_all()
        _run_seed()

    return app


def _run_seed():
    from models import Category, User
    categories = [
        Category(name="Alumbrado", icon="lightbulb", color_hex="#FFD700"),
        Category(name="Aseo", icon="trash", color_hex="#32CD32"),
        Category(name="Seguridad", icon="shield", color_hex="#FF4500"),
        Category(name="Servicios", icon="wrench", color_hex="#1E90FF"),
    ]
    for category in categories:
        existing = Category.query.filter_by(name=category.name).first()
        if not existing:
            db.session.add(category)

    test_user = User.query.filter_by(username="usuario_prueba").first()
    if not test_user:
        db.session.add(User(
            username="usuario_prueba",
            zone="Zona Centro",
            email="prueba@nodocivico.com"
        ))

    db.session.commit()
    print("✅ Base de datos poblada correctamente")


app = create_app()

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)