from flask import Blueprint, request, jsonify
from app.controllers.user_controller import (
    create_user_controller,
    authenticate_controller,
    get_user_by_id_controller,
    admin_get_all_users_controller,
    update_psw_controller,
    update_user_controller,
    reactivate_user_controller,
    deactivate_user_controller,
    admin_change_user_role_controller,
    admin_update_user_controller,
    admin_ban_user_controller,
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
        )
    ), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result = authenticate_controller(data["email"], data["password"])

    if not result["success"]:
        return jsonify({"message": result["message"]}), 401

    user = result["user"]
    token = generate_token(user.id, user.role)

    return (
        jsonify(
            {
                "message": "Login successful",
                "user": {"username": user.username, "token": token},
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
    return (
        jsonify(
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
            }
        ),
        200,
    )


@user_bp.route("/update", methods=["PUT"])
@jwt_required
def update_user(user_id, role):
    data = request.get_json()

    user = update_user_controller(user_id, data)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return (
        jsonify(
            {
                "message": "User updated successfully",
                "user_updated": {
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
        ),
        200,
    )


# dinguerie ça
@user_bp.route("/password", methods=["PUT"])
@jwt_required
def update_user_psw(user_id, role):
    data = request.get_json()
    result = update_psw_controller(user_id, data["new_psw"], data["old_psw"])

    status_code = 200 if result["success"] else 400
    return jsonify({"message": result["message"]}), status_code


@user_bp.route("/deactivate", methods=["POST"])
@jwt_required
def deactivate_user(user_id, role):
    result = deactivate_user_controller(user_id)
    status_code = 200 if result["success"] else 400
    return jsonify({"message": result["message"]}), status_code


@user_bp.route("/reactivate", methods=["POST"])
@jwt_required
def reactivate_user(user_id, role):

    result = reactivate_user_controller(user_id)

    status_code = 200 if result["success"] else 403

    if result["message"] == "User not found":
        status_code = 404

    elif result["message"] == "Account is already active":
        status_code = 400

    return jsonify({"message": result["message"]}), status_code


# --------------------admin--------------------
@user_bp.route("/admin/user", methods=["GET"])
@admin_required
def admin_get_all_users():
    users = admin_get_all_users_controller()
    return (
        jsonify(
            [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
                for user in users
            ]
        ),
        200,
    )


@user_bp.route("/admin/user/<int:target_user_id>", methods=["PATCH"])
@admin_required
def admin_update_user(target_user_id):
    data = request.get_json()

    user = admin_update_user_controller(target_user_id, data)

    if not user:
        return jsonify({"message": "user not found"}), 404

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


@user_bp.route("/admin/role/<int:target_user_id>", methods=["PATCH"])
@admin_required
def admin_change_role(target_user_id):

    data = request.get_json()
    if "role" not in data:
        return jsonify({"message": "Role is required"}), 400

    result = admin_change_user_role_controller(target_user_id, data["role"])
    return (
        jsonify(
            {
                "message": "User role updated successfully",
                "user": {
                    "id": result.id,
                    "username": result.username,
                    "new_role": result.role,
                },
            }
        ),
        200,
    )


@user_bp.route("/admin/ban/<int:target_user_id>", methods=["PATCH"])
@admin_required
def admin_ban_user(target_user_id):
    result = admin_ban_user_controller(target_user_id)

    status_code = 200 if result["success"] else 404

    return jsonify({"message": result["message"]}), status_code
