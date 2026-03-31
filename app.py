import streamlit as st
import time
import concurrent.futures
from core.prompts import PromptEngineer
from core.load_balancer import IntelligenceRouter
from utils.pdf_engine import PDFBuilder
from core.database import SupabaseManager

# ==========================================
# CONFIGURAÇÃO DE PÁGINA E ESTADO
# ==========================================
st.set_page_config(page_title="CONCL∆VE", page_icon="🔺", layout="centered", initial_sidebar_state="collapsed")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_kit' not in st.session_state:
    st.session_state.selected_kit = None
if 'selected_area' not in st.session_state:
    st.session_state.selected_area = None
if 'dossier' not in st.session_state:
    st.session_state.dossier = []
if 'verdict' not in st.session_state:
    st.session_state.verdict = ""

# ==========================================
# DESIGN SYSTEM CORPORATIVO (CSS ADAPTÁVEL)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    
    /* Ocultar elementos do Streamlit */
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}    
    header {visibility: hidden;}    

    /* Títulos e Branding */
    .brand-header { text-align: center; font-size: 2.8em; font-weight: 800; letter-spacing: -1px; margin-bottom: 2rem; }
    .brand-footer { text-align: center; font-size: 0.85em; color: #888; margin-top: 4rem; font-weight: 400; border-top: 1px solid #444; padding-top: 1rem;}
    .laranja-cria { color: #E85D04; }

    /* Botões Premium */
    .stButton>button {
        border-radius: 6px; font-weight: 600; transition: all 0.3s ease; height: 3rem;
    }
    .stButton>button:hover {
        border-color: #E85D04; color: #E85D04; box-shadow: 0 4px 12px rgba(232, 93, 4, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# CABEÇALHO GLOBAL
st.markdown('<div class="brand-header">CONCL<span class="laranja-cria">∆</span>VE</div>', unsafe_allow_html=True)

# ==========================================
# DEFINIÇÕES DE DADOS (KITS E ÁREAS)
# ==========================================
KITS = {
    "Agressivo": "Foco implacável em resultados rápidos, corte de custos e tolerância zero a ineficiências operacionais.",
    "Racional": "Análise fria baseada estritamente em dados, probabilidade, estatística e mitigação lógica de riscos.",
    "Diplomático": "Foco na cultura organizacional, contenção de danos de RP, estabilidade e transições corporativas suaves.",
    "Pragmático": "Busca pelo viável imediato. Foco em execução rápida, uso de recursos disponíveis e soluções 'pé no chão'.",
    "Disruptivo": "Quebra de paradigmas do mercado. Foco em inovação radical, alto risco e alto retorno estrutural."
}

AREAS = {
    "Administrativa e de Negócios": "Atua na otimização de processos, alocação de capital, ROI, EBITDA e eficiência corporativa.",
    "Jurídica, Leis e Compliance": "Focada na mitigação de passivos ocultos, adequação à LGPD, contratos e segurança jurídica.",
    "Social, ONGs e Impacto Comunitário": "Analisa o SROI (Retorno Social), Teoria da Mudança e impacto sem assistencialismo cego.",
    "Tecnologia e Transformação Digital": "Lida com Dívida Técnica, arquitetura de sistemas, segurança da informação e adoção de inovações.",
    "Psicológica e Recursos Humanos": "Foca na segurança psicológica, People Analytics, contenção de Burnout e cultura de alta performance."
}

# ==========================================
# ROTEADOR DE TELAS (WIZARD)
# ==========================================

# --- TELA 1: BOAS-VINDAS ---
if st.session_state.step == 1:
    st.markdown("<h3 style='text-align: center; font-weight: 300;'>Seja bem-vindo ao Hub de Decisão.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; max-width: 600px; margin: 0 auto 30px auto;'>Aqui é onde você consegue analisar suas questões ou problemas corporativos de múltiplas facetas simultaneamente, da forma mais sincera e analítica possível, através do Método CRÏ∆.</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("COMEÇAR SESSÃO", type="primary", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# --- TELA 2: ESCOLHA DO KIT ---
elif st.session_state.step == 2:
    st.markdown("### Passo 1: O Tom da Diretoria")
    st.markdown("Selecione qual será o **Kit de Comportamento** (a lente de mentalidade) que guiará a mesa de conselheiros.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for kit_name, kit_desc in KITS.items():
        with st.container(border=True):
            st.markdown(f"#### {kit_name}")
            st.write(kit_desc)
            if st.button(f"Selecionar Kit {kit_name}", key=f"btn_{kit_name}", use_container_width=True):
                st.session_state.selected_kit = kit_name
                st.session_state.step = 3
                st.rerun()
                
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Voltar"):
        st.session_state.step = 1
        st.rerun()

# --- TELA 3: ESCOLHA DA ÁREA ---
elif st.session_state.step == 3:
    st.markdown("### Passo 2: O Domínio de Especialidade")
    st.markdown(f"Kit selecionado: **{st.session_state.selected_kit}**. Agora, escolha a área de conhecimento que fundamentará a base de dados técnica do Conclave.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for area_name, area_desc in AREAS.items():
        with st.container(border=True):
            st.markdown(f"#### {area_name}")
            st.write(f"**Olá, sou a área que atua no assunto de {area_name}.** {area_desc}")
            if st.button(f"Selecionar {area_name}", key=f"btn_{area_name}", use_container_width=True):
                st.session_state.selected_area = area_name
                st.session_state.step = 4
                st.rerun()
                
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Voltar"):
        st.session_state.step = 2
        st.rerun()

# --- TELA 4: EXECUÇÃO DO MOTOR SECI COM MULTITHREADING ---
elif st.session_state.step == 4:
    st.markdown("### Passo 3: O Dilema Central")
    st.markdown(f"**Parâmetros Ativos:** Tom _{st.session_state.selected_kit}_ | Área: _{st.session_state.selected_area}_")
    
    user_dilemma = st.text_area("Descreva o cenário, problema ou decisão corporativa a ser tomada:", height=180)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Voltar"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        run_engine = st.button("EXECUTAR MOTOR SECI", type="primary", use_container_width=True)

    if run_engine:
        if not user_dilemma:
            st.warning("Por favor, insira o contexto do dilema.")
        else:
            st.session_state.dossier = []
            history_context = f"DILEMA ORIGINAL: {user_dilemma}\n\n"
            
            agents = [
                ("FASE I: Estratégico", "estrategista"), 
                ("FASE I: Humano", "humanista"), 
                ("FASE I: Analítico", "analista"), 
                ("FASE II: Inovador", "inovador"), 
                ("FASE III: Antagonista", "antagonista"), 
                ("FASE IV: Diplomata", "diplomata")
            ]

            st.markdown("---")
            st.markdown("### Deliberação da Mesa")

            # Função isolada para rodar nas Threads
            def process_agent(fase_nome, agent_id, area, kit, dilemma):
                prompt = PromptEngineer.build_prompt(area, agent_id, KITS[kit])
                context = f"DILEMA ORIGINAL: {dilemma}\n\n"
                resposta = IntelligenceRouter.execute_inference(prompt, context)
                return {"fase": fase_nome, "role": agent_id, "texto": resposta}

            resultados_agentes = []

            # ---------------------------------------------------------
            # MULTITHREADING + ACTIVE WAIT UX
            # ---------------------------------------------------------
            with st.status("Iniciando deliberação paralela dos conselheiros...", expanded=True) as status:
                st.write("⏳ Conectando aos agentes especializados simultaneamente...")
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                    futuros = {
                        executor.submit(process_agent, f_nome, a_id, st.session_state.selected_area, st.session_state.selected_kit, user_dilemma): (f_nome, a_id)
                        for f_nome, a_id in agents
                    }
                    
                    for future in concurrent.futures.as_completed(futuros):
                        f_nome, a_id = futuros[future]
                        try:
                            resultado = future.result()
                            resultados_agentes.append(resultado)
                            st.write(f"✅ O **{a_id.upper()}** concluiu a análise.")
                        except Exception as e:
                            st.write(f"❌ Ocorreu um gargalo com o **{a_id.upper()}**: {str(e)}")

                status.update(label="Análise isolada concluída com sucesso!", state="complete", expanded=False)

            # Reorganiza os resultados na ordem oficial das Fases para o PDF e para o Contexto
            ordem_oficial = {a_id: i for i, (f_nome, a_id) in enumerate(agents)}
            resultados_agentes.sort(key=lambda x: ordem_oficial[x['role']])

            for res in resultados_agentes:
                history_context += f"\n\n--- {res['fase']} ({res['role'].upper()}) ---\n{res['texto']}"
                st.session_state.dossier.append(res)
                with st.expander(f" {res['fase']} | {res['role'].upper()}", expanded=False):
                    st.markdown(res['texto'])

            # ---------------------------------------------------------
            # EXECUÇÃO FASE V: CONSENSO 
            # ---------------------------------------------------------
            with st.spinner("Sintetizando FASE V: Consenso..."):
                prompt_consenso = "Faça um resumo executivo dos pontos de concordância e discordância da mesa."
                resposta_consenso = IntelligenceRouter.execute_inference(prompt_consenso, history_context)
                history_context += f"\n\n--- FASE V: Consenso ---\n{resposta_consenso}"
                st.session_state.dossier.append({"fase": "FASE V: Consenso", "role": "diretoria", "texto": resposta_consenso})
                with st.expander(" FASE V: CONSENSO DA DIRETORIA", expanded=False):
                    st.markdown(resposta_consenso)

            st.markdown("---")
            st.markdown("### VEREDITO FINAL (FASE VI)")
            
            # ---------------------------------------------------------
            # EXECUÇÃO FASE VI E PERSISTÊNCIA
            # ---------------------------------------------------------
            with st.spinner("Compilando Plano Executivo e Canvas..."):
                prompt_decisor = PromptEngineer.build_prompt(st.session_state.selected_area, "decisor", KITS[st.session_state.selected_kit])
                verdict_text = IntelligenceRouter.execute_inference(prompt_decisor, history_context, "deep")
                st.session_state.verdict = verdict_text
                st.success(verdict_text)
                
                SupabaseManager.save_deliberation(st.session_state.selected_area, user_dilemma, verdict_text, st.session_state.selected_kit)

            # ---------------------------------------------------------
            # GERAÇÃO DO DOSSIÊ PDF
            # ---------------------------------------------------------
            with st.spinner("Gerando Dossiê Executivo (PDF)..."):
                caminho_pdf = PDFBuilder.generate_pdf(
                    area=st.session_state.selected_area, dilemma=user_dilemma,
                    dossier_data=st.session_state.dossier, verdict_data=st.session_state.verdict
                )
                with open(caminho_pdf, "rb") as f:
                    pdf_bytes = f.read()
                
                st.download_button(label="BAIXAR DOSSIÊ EXECUTIVO", data=pdf_bytes, file_name="Dossie_Conclave.pdf", mime="application/pdf", type="primary", use_container_width=True)

# RODAPÉ GLOBAL
st.markdown('<div class="brand-footer">Desenvolvido a base do método CR<span class="laranja-cria">Ï</span><span class="laranja-cria">∆</span></div>', unsafe_allow_html=True)