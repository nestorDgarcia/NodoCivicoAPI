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
        from seed import seed_database
        seed_database()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)