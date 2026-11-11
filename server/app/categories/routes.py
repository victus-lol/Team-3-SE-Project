"""
Category routes.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01)
"""

from flask import Blueprint, jsonify
from flask_login import current_user

from ..common.responses import success_response
from ..middleware.authorization import login_required_json
from .service import list_categories as get_categories

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("", methods=["GET"])
@login_required_json
def list_categories():
    categories = get_categories(current_user.id)

    return jsonify(
        success_response([
            category.to_dict()
            for category in categories
        ])
    ), 200


@categories_bp.route("", methods=["POST"])
@login_required_json
def create_category():
    return jsonify({
        "success": False,
        "error": {
            "code": "NOT_IMPLEMENTED",
            "message": "Category creation is pending scope approval.",
        },
    }), 501