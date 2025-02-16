from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Flask server is running!", 200

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"