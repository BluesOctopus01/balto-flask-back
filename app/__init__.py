from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()

migrate = Migrate()


def create_app():

    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # TODO model, route, register
    from app.models.user import User
    from app.models.deck import Deck
    from app.models.card_models.card_qcm import Qcm, Card
    from app.models.card_models.card_gapfill import Gapfill
    from app.models.card_models.card_answer_qcm import AnswerQcm
    from app.models.card_models.card_image import Image
    from app.models.card_models.card_qa import Qa

    return app
