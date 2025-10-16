from flask import Blueprint, request, jsonify
from app.controllers.user_controller import (
    create_user_controller,
    authenticate_controller,
    get_user_by_id_controller,
    get_all_user_controller,
    update_psw_controller,
    update_user_controller,
    change_user_role_controller,
    reactivate_user_controller,
    deactivate_user_controller,
)
from app.utils.jwt_utils import jwt_required, admin_required, generate_token

user_bp = Blueprint("user_bp", __name__, url_prefix="/users")


@user_bp.route("/", methods=["POST"])
def register_user():
    data = request.get_json()
    user = create_user_controller(data)

    if not user:
        return jsonify({"message": "User creation failed"}), 400

    elif user:
        token = generate_token(user.id, user.role)
    return (
        jsonify(
            {
                "username": user.username,
                "token": token,
            }
        ),
        201,
    )


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = authenticate_controller(data["email"], data["password"])
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_token(user.id, user.role)
    return (
        jsonify(
            {
                "username": user.username,
                "token": token,
            }
        ),
        200,
    )


@user_bp.route("/details", methods=["GET"])
@jwt_required
# revoie
def get_user(user_id, role):
    user = get_user_by_id_controller(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    # TODO A PERSONNALISE
    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }
    )
