from fpdf import FPDF

def generate_pdf_report(data, output_path):
    """
    Generate a PDF report from the given data.

    Args:
        data (dict): The data to include in the report.
        output_path (str): The path to save the PDF report.

    Returns:
        str: The path to the generated PDF report.
    """
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Reconnaissance Report", ln=True, align='C')
        pdf.ln(10)

        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

        pdf.output(output_path)
        return output_path
    except Exception as e:
        return f"Error in generating report: {str(e)}"
