from sqlalchemy import true
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
    return User.query.get(user_id)


def update_user_controller(user_id, data):
    updated_user = User.query.get(user_id)
    if not updated_user:
        return None


def update_psw_controller():
    pass


def delete_user_controller():
    pass


def get_all_user_controller():
    pass


def change_user_role_controller():
    pass
