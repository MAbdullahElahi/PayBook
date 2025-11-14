# Project title         :  Pay Book – Billing and Invoice Generator
# Project for           :  IT Fundamentals and Applications
# Project completed by  :  Muhammad Abdullah Elahi, TC-061
# Project submitted to  :  Dr. Amir Zeb, Lab Instructor and Class Teacher


# ────────────────────────────────────────────────
# 1. Import Required Modules
#    (ReportLab for PDF creation + datetime)
# ────────────────────────────────────────────────
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime



# ────────────────────────────────────────────────
# 2. Function: export_to_pdf(values, filename)
#    Generates a formatted PDF invoice using values dict
# ────────────────────────────────────────────────
def export_to_pdf(values, filename="invoice.pdf"):

    # ────────────────────────────────────────────
    # 2.1 Create auto-timestamped filename
    # ────────────────────────────────────────────
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # ensure lowercase extension consistency
    if filename.lower().endswith(".pdf"):
        filename = filename[:-4]  # remove .pdf (only the last 4 chars)

    # always add timestamp + .pdf
    filename = f"{filename}_{now}.pdf"

    # ────────────────────────────────────────────
    # 2.2 Initialize PDF Document
    # ────────────────────────────────────────────
    pdf = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    # Style collection and content container
    styles = getSampleStyleSheet()
    content = []


    # ────────────────────────────────────────────
    # 3. Title Section
    # ────────────────────────────────────────────
    title_style = ParagraphStyle(
        name="Title",
        fontSize=18,
        leading=22,
        alignment=1,   # center
        textColor=colors.HexColor("#daa53a"),
        spaceAfter=20
    )

    content.append(Paragraph("📘 PROJECT BILL SUMMARY", title_style))


    # ────────────────────────────────────────────
    # 4. General Information Section
    # ────────────────────────────────────────────
    info_style = ParagraphStyle(name="Info", fontSize=11, leading=16)

    general_info_keys = ["Project Name", "Client Name", "Date", "Objective", "Time"]

    # Print only available fields
    for key in general_info_keys:
        if key in values:
            content.append(Paragraph(f"<b>{key}:</b> {values[key]}", info_style))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>🧾 Services Provided</b>", styles["Heading4"]))
    content.append(Spacer(1, 6))


    # ────────────────────────────────────────────
    # 5. Services Table
    # ────────────────────────────────────────────
    if "Services" in values and len(values["Services"]) > 0:

        # Header row
        table_data = [["#", "Service/ Product", "Amount (PKR)", "Discount (%)", "Total (PKR)"]]

        # Add each service row
        for i, s in enumerate(values["Services"]):
            table_data.append([
                str(i + 1),
                s["Service/ Product"],
                f"{s['Amount (PKR)']:,.2f}",
                f"{s['Discount (%)']:,.2f}",
                f"{s['Total (PKR)']:,.2f}"
            ])

        # Create table with fixed widths
        table = Table(table_data, colWidths=[25, 180, 100, 100, 100])

        # Apply table styling
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#183f6b")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        content.append(table)

    else:
        # No services message
        content.append(Paragraph("No services added.", info_style))


    # ────────────────────────────────────────────
    # 6. Billing Summary Section
    # ────────────────────────────────────────────
    content.append(Spacer(1, 20))
    content.append(Paragraph("<b>💰 Billing Summary</b>", styles["Heading4"]))
    content.append(Spacer(1, 6))

    total = values["Total Amount (PKR)"]
    advance = values["Advance"]
    remaining = total - advance

    # Prepare summary rows
    summary_data = [
        ["Total Amount (PKR)", f"{total:,.2f}"],
        ["Advance (50%)", f"{advance:,.2f}"],
        ["Remaining Balance", f"{remaining:,.2f}"],
    ]

    # Create summary table
    summary_table = Table(summary_data, colWidths=[200, 120])

    # Style summary table
    summary_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#E5E8E8")),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    content.append(summary_table)


    # ────────────────────────────────────────────
    # 7. Generate & Save PDF
    # ────────────────────────────────────────────
    pdf.build(content)

    print(f"✅ PDF file saved successfully as: {filename}")
