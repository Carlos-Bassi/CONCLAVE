from fpdf import FPDF
from datetime import datetime
import os

class PDFBuilder:
    @staticmethod
    def generate_pdf(area: str, dilemma: str, dossier_data: list, verdict_data: str) -> str:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Cabeçalho Branding
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(232, 93, 4) # Laranja CRÏA
        pdf.cell(0, 10, "CONCLAVE | DOSSIE EXECUTIVO", ln=True, align='C')
        
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, f"Area: {area} | Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
        pdf.ln(10)
        
        # O Dilema
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "O DILEMA:", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, dilemma)
        pdf.ln(5)
        
        # Deliberações
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "DELIBERACAO DOS CONSELHEIROS:", ln=True)
        
        for item in dossier_data:
            pdf.set_font("Arial", 'B', 11)
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(0, 8, f"{item['fase']} | {item['role'].upper()}", ln=True, fill=True)
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 6, item['texto'])
            pdf.ln(4)
            
        # Veredito Final
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(232, 93, 4)
        pdf.cell(0, 10, "VEREDITO DA DIRETORIA (FASE VI)", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 7, verdict_data)
        
        output_path = "Dossie_Conclave.pdf"
        pdf.output(output_path)
        return output_path