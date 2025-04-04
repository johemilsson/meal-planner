from fpdf import FPDF

def create_recipe_pdf(title, ingredients, instructions, time, servings, file_name):
    # Initialize PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 8, title, ln=True, align='C')

    # Time and Servings
    pdf.set_font("Arial", '', 10)
    pdf.cell(200, 8, f"Tillagningstid: {time['amount']} {time['unit']}", ln=True)
    pdf.cell(200, 8, f"Portioner: {servings}", ln=True)

    # Ingredients
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, "Ingredienser:", ln=True)

    pdf.set_font("Arial", '', 10)
    for section, items in ingredients.items():
        pdf.cell(200, 8, f"{section}:", ln=True)
        for item in items:
            for name, details in item.items():
                pdf.cell(200, 8, f"- {name}: {details['amount']} {details['unit']}", ln=True)

    # Instructions
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, "Instruktioner:", ln=True)

    pdf.set_font("Arial", '', 10)
    for section, steps in instructions.items():
        pdf.cell(200, 8, f"{section}:", ln=True)
        for step in steps:
            pdf.cell(200, 8, f"- {step}", ln=True)

    # Save PDF
    pdf.output(file_name)