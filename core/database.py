from supabase import create_client, Client
from core.config import EnvManager
import logging

class SupabaseManager:
    """
    Arquiteto CRÏA: Conector do Supabase.
    Salva e recupera o histórico de deliberações para auditoria.
    """
    
    @staticmethod
    def get_client() -> Client:
        creds = EnvManager.get_supabase_credentials()
        return create_client(creds["url"], creds["key"])

    @staticmethod
    def save_deliberation(area: str, dilemma: str, verdict: str, kit: str):
        """Salva o dilema e o Veredito Final no banco de dados."""
        try:
            supabase = SupabaseManager.get_client()
            data = {
                "area_analise": area,
                "dilema": dilemma,
                "veredito": verdict,
                "kit_usado": kit,
                "pdf_gerado": True
            }
            supabase.table("conclave_history").insert(data).execute()
            logging.info("SaaS CRÏA: Deliberação salva no Supabase com sucesso.")
            return True
        except Exception as e:
            logging.error(f"SaaS CRÏA: Falha ao salvar no banco de dados. Erro: {str(e)}")
            return False

    @staticmethod
    def get_history(limit: int = 5):
        """Busca as deliberações mais recentes para a Sidebar."""
        try:
            supabase = SupabaseManager.get_client()
            response = supabase.table("conclave_history").select("*").order("created_at", desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            logging.error(f"SaaS CRÏA: Falha ao buscar histórico. Erro: {str(e)}")
            return []