from flask import Blueprint, jsonify
from models import Category
from schemas import serialize_category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify({
        "categories": [serialize_category(c) for c in categories]
    }), 200