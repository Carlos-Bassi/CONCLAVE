import os
import random
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class EnvManager:
    """
    Arquiteto CRÏA: Cofre Central de Configurações.
    Motor Híbrido: Lê tanto do .env local quanto do st.secrets da nuvem.
    """

    @staticmethod
    def get_keys(provider_prefix: str) -> list:
        keys = []
        
        # 1. Tenta ler direto do cofre do Streamlit Cloud (NUVEM)
        try:
            for i in range(1, 10):
                key_name = f"{provider_prefix}_API_KEY_{i}"
                if key_name in st.secrets:
                    keys.append(st.secrets[key_name])
            
            # Busca sem numeração (caso tenha cadastrado sem o _1)
            key_name_default = f"{provider_prefix}_API_KEY"
            if key_name_default in st.secrets and st.secrets[key_name_default] not in keys:
                keys.append(st.secrets[key_name_default])
        except Exception:
            pass

        # 2. Se não achou na nuvem, tenta no .env (LOCAL)
        if not keys:
            for i in range(1, 10):
                k = os.getenv(f"{provider_prefix}_API_KEY_{i}")
                if k: keys.append(k)
            
            k_default = os.getenv(f"{provider_prefix}_API_KEY")
            if k_default and k_default not in keys:
                keys.append(k_default)

        return keys

    @staticmethod
    def get_supabase_credentials() -> dict:
        url = None
        key = None
        
        # 1. Tenta via Streamlit Secrets
        try:
            if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
                url = st.secrets["SUPABASE_URL"]
                key = st.secrets["SUPABASE_KEY"]
        except Exception:
            pass

        # 2. Fallback para o .env local
        if not url or not key:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("FALHA CRÍTICA: Credenciais do Supabase ausentes.")

        return {"url": url, "key": key}

    # ========================================================
    # Adaptadores Legado (Para garantir que nada quebre)
    # ========================================================
    @staticmethod
    def get_groq_key() -> str:
        keys = EnvManager.get_keys("GROQ")
        if not keys: raise ValueError("Sem chave GROQ")
        return random.choice(keys)

    @staticmethod
    def get_gemini_key() -> str:
        keys = EnvManager.get_keys("GEMINI")
        if not keys: raise ValueError("Sem chave GEMINI")
        return random.choice(keys)

    @staticmethod
    def get_openrouter_key() -> str:
        keys = EnvManager.get_keys("OPENROUTER")
        if not keys: raise ValueError("Sem chave OPENROUTER")
        return random.choice(keys)