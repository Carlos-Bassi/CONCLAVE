import time
import logging
import re
from groq import Groq
from openai import OpenAI
import google.generativeai as genai
from core.config import EnvManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - LOAD BALANCER - %(levelname)s - %(message)s')

class IntelligenceRouter:
    
    @staticmethod
    def _execute_with_rotation(provider_name: str, keys: list, api_call_func) -> str:
        """Motor blindado: Tenta todas as chaves do provedor antes de reportar falha."""
        if not keys:
            raise ValueError(f"SaaS CRÏA: Nenhuma chave configurada para {provider_name}.")
        
        last_error = None
        for idx, key in enumerate(keys):
            try:
                # Executa a API com a chave do slot atual
                return api_call_func(key)
            except Exception as e:
                last_error = e
                erro_msg = str(e).lower()
                logging.warning(f"[{provider_name} Key {idx+1}/{len(keys)}] Esgotada/Falha. Motivo: {erro_msg}")
                
                # Se for limite de tokens, tenta a próxima chave na mesma hora
                if "rate limit" in erro_msg or "429" in erro_msg or "tokens" in erro_msg:
                    time.sleep(1)
                    continue
                else:
                    # Erro interno ou de conexão grave, aborta esse provedor
                    break 
        raise last_error

    @staticmethod
    def _call_groq(system_prompt: str, user_prompt: str) -> str:
        client = Groq(api_key=EnvManager.get_groq_key())
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # ATUALIZADO: Modelo novo de 70B
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=2000
        )
        return response.choices[0].message.content

    @staticmethod
    def _call_gemini(system_prompt: str, user_prompt: str) -> str:
        genai.configure(api_key=EnvManager.get_gemini_key())
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest", # ATUALIZADO: Rota segura
            system_instruction=system_prompt
        )
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.4)
        )
        return response.text

    @staticmethod
    def _call_openrouter(system_prompt: str, user_prompt: str) -> str:
        keys = EnvManager.get_keys("OPENROUTER")
        
        def make_call(key):
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)
            response = client.chat.completions.create(
                model="meta-llama/llama-3.1-70b-instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.4,
                max_tokens=2000
            )
            return response.choices[0].message.content
            
        return IntelligenceRouter._execute_with_rotation("OpenRouter", keys, make_call)

    @staticmethod
    def execute_inference(system_prompt: str, user_prompt: str, strategy: str = "fast") -> str:
        cascade_order = [
            ("Groq", IntelligenceRouter._call_groq),
            ("Gemini", IntelligenceRouter._call_gemini),
            ("OpenRouter", IntelligenceRouter._call_openrouter)
        ]

        erro_track = []

        for provider_name, call_function in cascade_order:
            try:
                logging.info(f"Roteando tráfego para {provider_name}...")
                raw_text = call_function(system_prompt, user_prompt)
                return IntelligenceRouter.sanitize_output(raw_text)
            except Exception as e:
                erro_track.append(f"{provider_name}: {str(e)}")
                logging.error(f"Cascata {provider_name} exaurida.")
                time.sleep(1.5) 

        # Dano crítico isolado: Interface do usuário não quebra.
        logging.error(f"FALHA GERAL DE INFRA: {erro_track}")
        return "VEREDITO DE INFRAESTRUTURA: Ocorreu um gargalo massivo de requisições nos servidores de IA. O Circuit Breaker do Conclave conteve a falha sistêmica. A integridade do software foi mantida. Aguarde 60 segundos para renovação de banda e tente novamente."

    @staticmethod
    def sanitize_output(text: str) -> str:
        if not text: return ""
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text) 
        text = re.sub(r'#{1,6}\s?', '', text)       
        text = re.sub(r'<[^>]+>', '', text)         
        return text.strip()