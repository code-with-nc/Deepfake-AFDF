from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def generate_report(file_path, res):
    report_path = file_path + "_Forensic_Report.pdf"
    c = canvas.Canvas(report_path, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "DEEPFAKE FORENSIC ANALYSIS REPORT")
    c.line(50, 745, 550, 745)
    
    # 1. Integrity
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 720, "1. Chain of Custody & Integrity")
    c.setFont("Helvetica", 10)
    c.drawString(60, 705, f"File Name: {res['filename']}")
    c.drawString(60, 690, f"SHA-256 Hash: {res['sha256']}")
    
    # 2. Findings
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 660, "2. Forensic Findings")
    c.setFont("Helvetica", 10)
    y = 645
    for key, val in res.items():
        if key not in ['filename', 'sha256', 'ela_visual']:
            c.drawString(60, y, f"{key.replace('_',' ').title()}: {val}")
            y -= 15

    # 3. Visual Artifacts (ELA)
    if 'ela_visual' in res:
        c.drawString(50, y-20, "3. Artifact Visualization (ELA Map):")
        c.drawImage(res['ela_visual'], 50, y-150, width=200, preserveAspectRatio=True)
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 50, "This report is computer-generated for forensic screening purposes.")
    
    c.save()
    return report_path