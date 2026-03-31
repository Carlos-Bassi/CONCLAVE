import os
import random
from dotenv import load_dotenv

load_dotenv()

class EnvManager:
    """
    Arquiteto CRIA: Cofre Central de Configuracoes.
    Motor de rodizio universal para evitar falhas de Rate Limit.
    """

    @staticmethod
    def _get_random_key(provider_prefix: str) -> str:
        """Busca as duas chaves do provedor e sorteia uma valida."""
        keys = [
            os.getenv(f"{provider_prefix}_API_KEY_1"),
            os.getenv(f"{provider_prefix}_API_KEY_2")
        ]
        valid_keys = [k for k in keys if k]
        
        if not valid_keys:
            raise ValueError(f"FALHA CRITICA: Nenhuma chave {provider_prefix} encontrada no .env")
        
        import os
from dotenv import load_dotenv

load_dotenv()

class EnvManager:
    """
    Arquiteto CRÏA: Cofre Central de Configurações.
    Motor de rodízio de chaves em Pool para blindagem contra Rate Limit.
    """

    @staticmethod
    def get_keys(provider_prefix: str) -> list:
        """Busca todas as chaves declaradas e retorna uma matriz de redundância."""
        keys = []
        # Procura por múltiplas chaves enumeradas no .env (até 10 redundâncias)
        for i in range(1, 10):
            k = os.getenv(f"{provider_prefix}_API_KEY_{i}")
            if k: keys.append(k)
        
        # Procura pelo padrão normal sem número
        k_default = os.getenv(f"{provider_prefix}_API_KEY")
        if k_default and k_default not in keys:
            keys.append(k_default)
            
        return keys

    @staticmethod
    def get_supabase_credentials() -> dict:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("FALHA CRÍTICA: Credenciais do Supabase ausentes.")
        return {"url": url, "key": key}
    @staticmethod
    def get_groq_key() -> str:
        return EnvManager._get_random_key("GROQ")

    @staticmethod
    def get_gemini_key() -> str:
        return EnvManager._get_random_key("GEMINI")

    @staticmethod
    def get_cohere_key() -> str:
        return EnvManager._get_random_key("COHERE")

    @staticmethod
    def get_sambanova_key() -> str:
        return EnvManager._get_random_key("SAMBANOVA")

    @staticmethod
    def get_cerebras_key() -> str:
        return EnvManager._get_random_key("CEREBRAS")

    @staticmethod
    def get_openrouter_key() -> str:
        return EnvManager._get_random_key("OPENROUTER")

    @staticmethod
    def get_huggingface_key() -> str:
        return EnvManager._get_random_key("HUGGINGFACE")

    @staticmethod
    def get_supabase_credentials() -> dict:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("FALHA CRITICA: Credenciais do Supabase ausentes.")
        return {"url": url, "key": key}