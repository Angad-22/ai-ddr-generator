from fpdf import FPDF

class DDRPDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Detailed Diagnostic Report (DDR)", ln=True, align="C")
        self.ln(5)


def create_pdf(content, output_path):
    pdf = DDRPDF()
    pdf.add_page()

    lines = content.split("\n")

    for line in lines:

        line = line.strip()

        # Section headings (1. , 2. , etc.)
        if line.startswith(tuple(str(i) + "." for i in range(1, 8))):
            pdf.set_font("Arial", "B", 13)
            pdf.ln(3)
            pdf.multi_cell(0, 8, line)

        # Sub-headings (Hall:, Bedroom:, etc.)
        elif line.endswith(":"):
            pdf.set_font("Arial", "B", 11)
            pdf.multi_cell(0, 7, line)

        # Normal text
        else:
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 7, line)

    pdf.output(output_path)