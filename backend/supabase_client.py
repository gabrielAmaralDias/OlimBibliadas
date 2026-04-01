from supabase import create_client, Client
from dotenv import load_dotenv
import os
import random

# Garante que o .env seja carregado aqui também
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL e SUPABASE_KEY não encontrados no .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def pegar_pergunta():
    try:
        # ✅ Nome da tabela exatamente igual ao do Supabase
        dados = supabase.table("TB_perguntas").select("id, Pergunta, Reposta").execute()
        if dados.data:
            return random.choice(dados.data)
        return None
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar pergunta: {str(e)}")