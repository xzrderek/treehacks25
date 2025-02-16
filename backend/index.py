from flask import Flask
from .routes import tinyagent_bp
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import enum
from flask_cors import CORS
from . import task_queue  # Add this import

# db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
CORS(app)

app.register_blueprint(tinyagent_bp)
# db.init_app(app)
# migrate.init_app(app, db)

# The task queue worker thread will start automatically when imported

@app.route("/")
def home():
    return "Flask server is running!", 200

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
