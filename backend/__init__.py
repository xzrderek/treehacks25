from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Flask server is running!", 200

    @app.route("/api/python")
    def hello_world():
        return "<p>Hello, World!</p>"
    # Use SQLite with local file storage
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "tasks.db")}'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # db.init_app(app)
    
    # with app.app_context():
    #     db.create_all()  # Create tables if they don't exist

    from .routes import api
    app.register_blueprint(api)

    return app

