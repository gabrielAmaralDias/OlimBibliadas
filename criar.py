import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")  # ← corrigido: era SUPABASE_API_KEY

def criar_usuario(email, senha):
    url = f"{SUPABASE_URL}/auth/v1/admin/users"

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "password": senha,
        "email_confirm": True
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code in (200, 201):
        print("Usuário criado com sucesso!")
        print(response.json())
    else:
        print(f"Erro ao criar usuário: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    email = input("Email do usuário: ")
    senha = input("Senha do usuário: ")
    criar_usuario(email, senha)