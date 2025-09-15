from fpdf import FPDF
import json

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

def generate_markdown_report(data: dict, output_path: str) -> str:
    """
    Generates a Markdown report from the given data.

    Args:
        data (dict): The data to include in the report.
        output_path (str): The path to save the Markdown report.

    Returns:
        str: The path to the generated Markdown report.
    """
    try:
        with open(output_path, 'w') as f:
            f.write("# RedCalibur Reconnaissance Report\n\n")
            
            if "gemini_summary" in data:
                f.write("## AI-Powered Summary\n\n")
                f.write(data["gemini_summary"])
                f.write("\n\n")

            for section, content in data.items():
                if section == "gemini_summary":
                    continue
                f.write(f"## {section.replace('_', ' ').title()}\n\n")
                if isinstance(content, dict):
                    for key, value in content.items():
                        f.write(f"**{key.replace('_', ' ').title()}:**\n")
                        if isinstance(value, dict):
                            f.write("```json\n")
                            f.write(json.dumps(value, indent=2, default=str))
                            f.write("\n```\n\n")
                        elif isinstance(value, list):
                            for item in value:
                                f.write(f"- {item}\n")
                            f.write("\n")
                        else:
                            f.write(f"{value}\n\n")
                else:
                    f.write(f"{content}\n\n")
        return output_path
    except Exception as e:
        return f"Error in generating Markdown report: {str(e)}"
