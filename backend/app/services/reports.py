from fpdf import FPDF
from app.models.audit import Scan, Page
from typing import List

class ReportService:
    def generate_scan_pdf(self, scan: Scan, pages: List[Page]) -> bytes:
        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, txt="SEO Audit Report", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(190, 10, txt=f"Domain: {scan.domain}", ln=True, align='C')
        pdf.cell(190, 10, txt=f"Date: {scan.created_at.strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        pdf.cell(190, 10, txt=f"Overall Score: {round(scan.overall_score, 2)}", ln=True, align='C')

        pdf.ln(10)

        # Summary
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, txt="Page Breakdown", ln=True)
        pdf.set_font("Arial", size=10)

        for page in pages:
            pdf.cell(130, 8, txt=f"{page.url[:60]}...", border=1)
            pdf.cell(30, 8, txt=f"Score: {round(page.seo_score, 1)}", border=1)
            pdf.cell(30, 8, txt=f"Words: {page.word_count}", border=1, ln=True)

        return pdf.output()

report_service = ReportService()
