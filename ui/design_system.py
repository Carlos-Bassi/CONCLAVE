import streamlit as st

class UIDesignSystem:
    """
    Arquiteto CRÏA: Sistema de Design Corporativo Premium.
    Injeta tipografia, estilos de card e contorna as limitações visuais do Streamlit.
    """

    # Mapeamento de Ícones para as 9 Áreas (Exigência da Pergunta 21)
    AREA_ICONS = {
        "Administrativa e de Negócios": "📊",
        "Jurídica, Leis e Compliance": "⚖️",
        "Social, ONGs e Impacto Comunitário": "🤝",
        "Psicológica e Recursos Humanos": "🧠",
        "Tecnologia e Transformação Digital": "💻",
        "Vida Pessoal e Relacionamentos": "🏡",
        "Meio Ambiente e Sustentabilidade": "🌱",
        "Educação, Pesquisa e Academia": "📚",
        "Visão Sistêmica e Assuntos Gerais": "🌐"
    }

    @staticmethod
    def inject_premium_css():
        """Injeta o CSS global para garantir a identidade CRÏA (Dark/Light adaptativo)."""
        custom_css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=DM+Mono:wght@400;500&display=swap');
        
        /* Tipografia Global */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
        }

        /* Esconde elementos nativos do Streamlit que poluem a tela */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Estilização do Título Principal */
        .conclave-title {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -2px;
            margin-bottom: 0px;
            padding-bottom: 0px;
        }
        
        .conclave-subtitle {
            font-family: 'DM Mono', monospace;
            font-size: 0.9rem;
            color: #E85D04; /* Laranja CRÏA */
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 2rem;
        }

        /* Estilização dos Accordions (Sanfonas) - Pergunta 22 */
        [data-testid="stExpander"] {
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
            border-radius: 8px !important;
            background-color: transparent !important;
            margin-bottom: 10px !important;
            transition: all 0.2s ease-in-out;
        }
        [data-testid="stExpander"]:hover {
            border-color: #E85D04 !important;
        }
        
        /* Texto dentro do Accordion */
        .agent-text-block {
            font-size: 1rem;
            line-height: 1.7;
            text-align: justify;
            padding: 10px;
        }

        /* Estilização do Veredito Final (Destaque) */
        .verdict-box {
            border-left: 5px solid #E85D04;
            background: rgba(232, 93, 4, 0.05);
            padding: 20px;
            border-radius: 0px 8px 8px 0px;
            margin-top: 30px;
            margin-bottom: 30px;
        }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)

    @staticmethod
    def render_header():
        """Renderiza o cabeçalho oficial do Conclave."""
        st.markdown('<div class="conclave-title">CONCLAVE</div>', unsafe_allow_html=True)
        st.markdown('<div class="conclave-subtitle">Protocolo de Deliberação SECI</div>', unsafe_allow_html=True)

    @staticmethod
    def get_icon(area: str) -> str:
        """Retorna o ícone correto para a área selecionada."""
        return UIDesignSystem.AREA_ICONS.get(area, "⚡")

    @staticmethod
    def render_agent_accordion(agent_name: str, role_title: str, content: str):
        """
        Gera a 'Sanfona' (Accordion) para esconder textos grandes e manter a tela limpa.
        Utilizado nas Fases 1 a 5.
        """
        # st.expander cria a sanfona nativa do Streamlit
        with st.expander(f"» {agent_name.upper()} | {role_title}", expanded=False):
            st.markdown(f'<div class="agent-text-block">{content}</div>', unsafe_allow_html=True)

    @staticmethod
    def render_verdict_box(content: str):
        """Renderiza o Veredito da Diretoria em uma caixa de destaque absoluta."""
        st.markdown("### Veredito da Diretoria (Fase VI)")
        st.markdown(f'<div class="verdict-box">{content}</div>', unsafe_allow_html=True)