import os
from datetime import datetime

from django.conf import settings

from reportlab.lib.colors import red
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


# ---------------------------------------------------------
# Helper Function
# ---------------------------------------------------------

def draw_heading(pdf, title, y):
    """
    Draws a section heading.
    """

    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, y, title)

    return y - 25


# ---------------------------------------------------------

def draw_text(pdf, text, y, indent=0):
    """
    Draws normal text.
    """

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        50 + indent,
        y,
        str(text)
    )

    return y - 18


# ---------------------------------------------------------

def check_page(pdf, y):
    """
    Creates a new page when space is finished.
    """

    if y < 60:

        pdf.showPage()

        pdf.setFont("Helvetica", 11)

        return 750

    return y


# ---------------------------------------------------------
# PDF Generator
# ---------------------------------------------------------

def generate_pdf(report):
    """
    Generates a PDF report from the parsed MobSF report.

    Returns:
        Path of generated PDF.
    """

    reports_folder = os.path.join(
        settings.MEDIA_ROOT,
        "reports"
    )

    os.makedirs(reports_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{report['app_name']}_{timestamp}.pdf"

    pdf_path = os.path.join(
        reports_folder,
        filename
    )

    pdf = canvas.Canvas(
        pdf_path,
        pagesize=letter
    )

    width, height = letter

    y = 760

    # =====================================================
    # TITLE
    # =====================================================

    pdf.setTitle("MobSF Security Report")

    pdf.setFont("Helvetica-Bold", 22)

    title = "MobSF APK Security Report"

    title_width = stringWidth(
        title,
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        (width - title_width) / 2,
        y,
        title
    )

    y -= 45

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    y = draw_heading(pdf, "Application Information", y)

    y = draw_text(
        pdf,
        f"Application : {report.get('app_name')}",
        y
    )

    y = draw_text(
        pdf,
        f"APK File : {report.get('file_name')}",
        y
    )

    y = draw_text(
        pdf,
        f"Version : {report.get('version')}",
        y
    )

    y = draw_text(
        pdf,
        f"Hash : {report.get('hash')}",
        y
    )

    y -= 10

    # =====================================================
    # SUMMARY
    # =====================================================

    y = draw_heading(pdf, "Security Summary", y)

    y = draw_text(
        pdf,
        f"Security Score : {report.get('security_score')}",
        y
    )

    y = draw_text(
        pdf,
        f"Trackers : {report.get('trackers')}",
        y
    )

    y = draw_text(
        pdf,
        f"Total Trackers : {report.get('total_trackers')}",
        y
    )

    y -= 20

    # =====================================================
    # HIGH FINDINGS
    # =====================================================

    y = draw_heading(pdf, "High Severity Findings", y)

    high = report.get("high_findings", [])

    if not high:

        y = draw_text(
            pdf,
            "No High Severity Findings.",
            y
        )

    else:

        for finding in high:

            y = check_page(pdf, y)

            pdf.setFillColor(red)

            y = draw_text(
                pdf,
                f"• {finding.get('title')}",
                y
            )

            pdf.setFillColorRGB(0, 0, 0)

            y = draw_text(
                pdf,
                finding.get("description"),
                y,
                indent=20
            )

            y -= 8

    y -= 20

    # =====================================================
    # WARNINGS
    # =====================================================

    y = draw_heading(pdf, "Warnings", y)

    warnings = report.get("warnings", [])

    if not warnings:

        y = draw_text(
            pdf,
            "No Warnings.",
            y
        )

    else:

        for finding in warnings:

            y = check_page(pdf, y)

            y = draw_text(
                pdf,
                f"• {finding.get('title')}",
                y
            )

            y = draw_text(
                pdf,
                finding.get("description"),
                y,
                indent=20
            )

            y -= 8

    y -= 20

    # =====================================================
    # INFORMATIONAL FINDINGS
    # =====================================================

    y = draw_heading(pdf, "Informational Findings", y)

    infos = report.get("info", [])

    if not infos:

        y = draw_text(
            pdf,
            "No Informational Findings.",
            y
        )

    else:

        for finding in infos:

            y = check_page(pdf, y)

            y = draw_text(
                pdf,
                f"• {finding.get('title')}",
                y
            )

            y = draw_text(
                pdf,
                finding.get("description"),
                y,
                indent=20
            )

            y -= 8

    y -= 20

    # =====================================================
    # SECURE FINDINGS
    # =====================================================

    y = draw_heading(pdf, "Secure Findings", y)

    secure = report.get("secure", [])

    if not secure:

        y = draw_text(
            pdf,
            "None",
            y
        )

    else:

        for item in secure:

            y = check_page(pdf, y)

            y = draw_text(
                pdf,
                f"• {item.get('title')}",
                y
            )

            y = draw_text(
                pdf,
                item.get("description"),
                y,
                indent=20
            )

            y -= 8

    y -= 20

    # =====================================================
    # HOTSPOTS
    # =====================================================

    y = draw_heading(pdf, "Security Hotspots", y)

    hotspots = report.get("hotspots", [])

    if not hotspots:

        y = draw_text(
            pdf,
            "None",
            y
        )

    else:

        for item in hotspots:

            y = check_page(pdf, y)

            y = draw_text(
                pdf,
                f"• {item.get('title')}",
                y
            )

            y = draw_text(
                pdf,
                item.get("description"),
                y,
                indent=20
            )

            y -= 8

    y -= 20

    # =====================================================
    # EXPORTED COMPONENTS
    # =====================================================

    y = draw_heading(pdf, "Exported Components", y)

    components = report.get(
        "exported_components",
        {}
    )

    if not components:

        y = draw_text(
            pdf,
            "No Exported Components.",
            y
        )

    else:

        for key, value in components.items():

            y = check_page(pdf, y)

            y = draw_text(
                pdf,
                f"{key} : {value}",
                y
            )

    y -= 20

    # =====================================================
    # HARDCODED SECRETS
    # =====================================================

    y = draw_heading(pdf, "Hardcoded Secrets", y)

    secrets = report.get("secrets", [])

    if not secrets:

        y = draw_text(
            pdf,
            "No Secrets Found.",
            y
        )

    else:

        for secret in secrets:

            y = check_page(pdf, y)

            y = draw_text(
                pdf,
                secret,
                y
            )

    # =====================================================
    # FOOTER
    # =====================================================

    pdf.setFont(
        "Helvetica-Oblique",
        9
    )

    pdf.drawString(
        50,
        20,
        "Generated by APK Scanner using MobSF"
    )

    pdf.save()

    return pdf_path