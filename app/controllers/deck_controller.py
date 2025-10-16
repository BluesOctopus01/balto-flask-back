from app.models import db, Deck, User
from werkzeug.security import generate_password_hash, check_password_hash

# TODO gestion automatique Size par nombres de cartes par deck
# TODO gestion Acces pour Obliger certain type et gerer les access


def update_last_login_controller(deck):
    from datetime import datetime, timezone

    deck.last_modification_at = datetime.now(timezone.utc)
    db.session.commit()


def create_deck_controller(data, creator_id):

    new_deck = Deck(
        name=data["name"],
        bio=data["bio"],
        deck_image=data["deck_image"],
        creator_id=creator_id,
    )
    db.session.add(new_deck)
    db.session.commit()

    return new_deck


def get_deck_by_id_controller(deck_id):
    deck = Deck.query.get(deck_id)
    if deck:
        return deck
    return None


def get_deck_by_user_controller(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None
    decks = user.decks
    if decks:
        return decks
    return None


def update_deck_controller(deck_id, user_id, data):

    deck_to_update = Deck.query.filter_by(id=deck_id).first()
    user = User.query.filter_by(id=user_id).first()

    if not user or not deck_to_update:
        return None

    if user.id == deck_to_update.creator_id or user.role == "admin":

        deck_to_update.name = data.get("name", deck_to_update.name)
        deck_to_update.bio = data.get("bio", deck_to_update.name)
        deck_to_update.deck_image = data.get("deck_image", deck_to_update.name)

        db.session.commit()
        update_last_login_controller(deck_to_update)

        return deck_to_update


def update_access_deck_controller():
    pass


def update_access_key_deck_controller():
    pass


def deactivate_deck_controller():
    pass


def reactivate_deck_controller():
    pass


def get_all_public_decks_controller():
    pass


def get_all_decks_controller():
    pass
