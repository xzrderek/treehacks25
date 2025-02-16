from flask import Flask
from routes import tinyagent_bp

app = Flask(__name__)

app.register_blueprint(tinyagent_bp)

@app.route("/")
def home():
    return "Flask server is running!", 200

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(port=5000, debug=True)