from app import app
from models import db, Category, User

def seed_database():
    with app.app_context():
        # Categorías predefinidas
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

        # Usuario de prueba
        test_user = User.query.filter_by(username="usuario_prueba").first()
        if not test_user:
            test_user = User(
                username="usuario_prueba",
                zone="Zona Centro",
                email="prueba@nodocivico.com"
            )
            db.session.add(test_user)

        db.session.commit()
        print("✅ Base de datos poblada correctamente")

if __name__ == '__main__':
    seed_database()