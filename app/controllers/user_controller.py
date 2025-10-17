from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


def update_last_login_controller(user):
    from datetime import datetime, timezone

    user.last_login_at = datetime.now(timezone.utc)
    db.session.commit()


def create_user_controller(data):
    hashed_psw = generate_password_hash(data["password"])

    new_user = User(
        username=data["username"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        password=hashed_psw,
        email=data["email"],
        phone_number=data["phone_number"],
        birth_date=data["birth_date"],
        adress=data["adress"],
        user_bio=data["user_bio"],
        image=data["image"],
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user


def authenticate_controller(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        update_last_login_controller(user)
        return user
    return None


def get_user_by_id_controller(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    return None


def update_user_controller(user_id, data):
    updated_user = User.query.get(user_id)
    if not updated_user:
        return None
    updated_user.username = data.get("username", updated_user.username)
    updated_user.first_name = data.get("first_name", updated_user.first_name)
    updated_user.last_name = data.get("last_name", updated_user.last_name)
    updated_user.email = data.get("email", updated_user.email)
    updated_user.phone_number = data.get("phone_number", updated_user.phone_number)
    updated_user.address = data.get("address", updated_user.address)
    updated_user.user_bio = data.get("user_bio", updated_user.user_bio)
    updated_user.image = data.get("image", updated_user.image)
    # Ca ne fait pas de sens de pouvoir changer la date de naissance
    db.session.commit()
    return updated_user


def update_psw_controller(user_id, new_psw, old_psw):
    user = User.query.get(user_id)
    if not user:
        return {"success": False, "message": "User not found"}

    if not check_password_hash(user.password, old_psw):
        return {"success": False, "message": "Old password is incorrect"}

    if check_password_hash(user.password, new_psw):
        return {"success": False, "message": "You cannot reuse the old password"}

    try:
        user.password = generate_password_hash(new_psw)
        db.session.commit()
        return {"success": True, "message": "Password updated successfully"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Database error {str(e)}"}


def deactivate_user_controller(user_id, role):
    user_to_deactivate = User.query.get(user_id)
    if not user_to_deactivate:
        return {"success": False, "message": "User not found"}
    if not user_to_deactivate.is_active:
        return {"success": False, "message": "Account already deactivated"}
    if role == "admin" or user_id == user_to_deactivate.id:
        user_to_deactivate.is_active = False
        db.session.commit()
        return {
            "success": True,
            "message": "Password updated successfully",
            "user": user_to_deactivate,
        }


def reactivate_user_controller(user_id, role):
    user_to_reactivate = User.query.get(user_id)
    if not user_to_reactivate:
        return None
    if not user_to_reactivate.is_active:
        return None
    if user_to_reactivate.id == user_id or role == "admin":
        user_to_reactivate.is_active = True
        db.session.commit()
        return user_to_reactivate


def get_all_user_controller():
    return User.query.all()


def admin_change_user_role_controller(user_id, new_role):
    # Definir les roles autorisés
    valid_roles = ["user", "admin"]

    if new_role not in valid_roles:
        return {"error": "Invalid role"}

    user = User.query.get(user_id)
    if not user:
        return None

    try:
        user.role = new_role
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        return {"error": f"Database error {str(e)}"}


def admin_update_user_controller(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return None

    if "user_bio" in data:
        user.user_bio = data["user_bio"]

    if "image" in data:
        user.user_bio = data["image"]

    db.session.commit()
    return user
