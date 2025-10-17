from flask import Blueprint, request, jsonify
from app.controllers.user_controller import (
    create_user_controller,
    authenticate_controller,
    get_user_by_id_controller,
    get_all_user_controller,
    update_psw_controller,
    update_user_controller,
    reactivate_user_controller,
    deactivate_user_controller,
    admin_change_user_role_controller,
    admin_update_user_controller,
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
                "message": "User succesfully registered ",
                "user": {
                    "username": user.username,
                    "token": token,
                },
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
                "message": "Login succesfull",
                "user": {
                    "username": user.username,
                    "token": token,
                },
            }
        ),
        200,
    )


@user_bp.route("/details", methods=["GET"])
@jwt_required
# renvoie role et id a chaque fois
def get_user(user_id, role):
    user = get_user_by_id_controller(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(
        {
            "message": "User updated",
            "user": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "user_bio": user.user_bio,
                "image": user.image,
                "created_at": user.created_at,
                "last_login_at": user.last_login_at,
                "role": user.role,
            },
        },
        200,
    )


@user_bp.route("/update", methods=["PUT"])
@jwt_required
def update_self_user(user_id, role):
    data = request.get_json()

    user = update_user_controller(user_id, data)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {
            {
                "message": "User updated successfully",
                "user updated": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "address": user.address,
                    "user_bio": user.user_bio,
                    "image": user.image,
                    "created_at": user.created_at,
                    "last_login_at": user.last_login_at,
                    "role": user.role,
                },
            }
        },
        200,
    )


# --------------------admin--------------------


@user_bp.route("/admin/user/<int:user_id>", methods=["PATCH"])
@admin_required
def admin_update_user(user_id):
    data = request.get_json()

    user = admin_update_user_controller(user_id, data)

    if not user:
        return (jsonify({"message": "user not found"}),)

    return jsonify(
        {
            "message": "User updated successfully by admin",
            "user": {
                "id": user.id,
                "username": user.username,
                "user_bio": user.user_bio,
                "image": user.image,
            },
        }
    )
