from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI"
        )


    # Import models here for Alembic setup
    from app.models.user import User
    from app.models.place import Place
    from app.models.history import History

    db.init_app(app)
    migrate.init_app(app, db)
    from .routes import users_bp
    from .routes import places_bp
    from .routes import histories_bp

    # Register Blueprints here
    # from .routes import example_bp
    # app.register_blueprint(example_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(histories_bp)

    CORS(app)
    return app



