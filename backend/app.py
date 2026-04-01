from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    template_folder=os.path.join(FRONTEND_DIR, "html")
)
CORS(app)

sys.path.insert(0, BASE_DIR)
from supabase_client import pegar_pergunta

usuarios = {"admin": "123"}

@app.route("/")
def index():
    return send_from_directory(app.template_folder, "login.html")

@app.route("/<path:path>")
def serve_template(path):
    if path.startswith(("css/", "js/", "img/")):
        return app.send_static_file(path)

    template_path = os.path.join(app.template_folder, path)
    if os.path.exists(template_path):
        return send_from_directory(app.template_folder, path)

    return send_from_directory(app.template_folder, "login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        from supabase_client import supabase
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        token = response.session.access_token
        return jsonify({"access_token": token})
    except Exception as e:
        return jsonify({"erro": "Login inválido"}), 401
@app.route("/pergunta")
def get_pergunta():
    try:
        pergunta = pegar_pergunta()
    except RuntimeError as e:
        return jsonify({"erro": str(e)}), 500
    if not pergunta:
        return jsonify({"erro": "Sem perguntas"}), 404
    return jsonify(pergunta)

if __name__ == "__main__":
    app.run(debug=True)