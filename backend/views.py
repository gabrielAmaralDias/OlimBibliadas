from flask import request, jsonify, send_from_directory
from app import app
import os
from supabase_client import pegar_pergunta

# Usuários simulados
usuarios = {"admin": "123"}

# Serve HTML e arquivos estáticos do frontend
@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>", endpoint='catch_all')
def serve_template(path):
    # arquivos estáticos (css, js, img)
    if path.startswith(("css/", "js/", "img/")):
        return app.send_static_file(path)

    # HTML
    template_path = os.path.join(app.template_folder, path)
    if os.path.exists(template_path):
        return send_from_directory(app.template_folder, path)
    # fallback
    return send_from_directory(app.template_folder, "index.html")


# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username") or data.get("email")
    password = data.get("password")

    if usuarios.get(username) == password:
        return jsonify({"access_token": "token_simulado"})
    return jsonify({"erro": "Login inválido"}), 401


# Pergunta (puxa do Supabase)
@app.route("/pergunta")
def get_pergunta():
    try:
        pergunta = pegar_pergunta()
    except RuntimeError as e:
        return jsonify({"erro": str(e)}), 500

    if not pergunta:
        return jsonify({"erro": "Sem perguntas"}), 404

    return jsonify(pergunta)
