import matplotlib.pyplot as plt
import numpy as np
import io
import base64

class ChartEngine:
    """
    Arquiteto CRÏA: Motor de Gráficos Dinâmicos.
    Gera o Radar Científico em Base64 para injeção nativa no HTML/PDF.
    """

    @staticmethod
    def generate_radar_b64(area: str) -> str:
        # Eixos dinâmicos baseados na Área (Exigência SECI)
        if area == "Jurídica, Leis e Compliance":
            labels = ['Passivo Legal', 'Risco de Imagem', 'Custo Operacional', 'Inovação', 'Viabilidade']
            values = [80, 60, 40, 30, 70]
        elif area == "Social, ONGs e Impacto Comunitário":
            labels = ['Risco de Greenwashing', 'Impacto Real (SROI)', 'Engajamento', 'Custo', 'Escalabilidade']
            values = [90, 20, 40, 85, 30]
        elif area == "Tecnologia e Transformação Digital":
            labels = ['Dívida Técnica', 'Inovação', 'Escalabilidade', 'Custo Cloud', 'Adoção']
            values = [85, 90, 70, 60, 50]
        else:
            labels = ['Risco Financeiro', 'Inovação', 'Viabilidade Técnica', 'Atrito Cultural', 'Tempo de Retorno']
            values = [70, 80, 50, 60, 40]
            
        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        values += values[:1]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        
        # SOLUÇÃO DEFINITIVA: Fundo Branco Sólido (Bypassa o bug de transparência do Matplotlib)
        fig.patch.set_facecolor('white') 
        ax.set_facecolor('white')
        
        plt.xticks(angles[:-1], labels, color='#333333', size=9, family='sans-serif')
        ax.set_rlabel_position(0)
        plt.yticks([20, 40, 60, 80], ["20", "40", "60", "80"], color="#AAAAAA", size=7)
        plt.ylim(0, 100)
        
        ax.plot(angles, values, linewidth=2, linestyle='solid', color='#E85D04')
        ax.fill(angles, values, '#E85D04', alpha=0.3)
        
        buf = io.BytesIO()
        plt.tight_layout()
        
        # Removido o parâmetro transparent=True
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        plt.close()
        
        return base64.b64encode(buf.getvalue()).decode('utf-8')