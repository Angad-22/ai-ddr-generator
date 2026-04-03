from flask import Flask, render_template, request, send_file
import os

from utils.extractor import extract_text
from utils.ai_processor import generate_ddr
from utils.report_generator import create_pdf
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        inspection_file = request.files["inspection"]
        thermal_file = request.files["thermal"]

        inspection_path = os.path.join(UPLOAD_FOLDER, inspection_file.filename)
        thermal_path = os.path.join(UPLOAD_FOLDER, thermal_file.filename)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        inspection_file.save(inspection_path)
        thermal_file.save(thermal_path)

        # Extract text
        inspection_text = extract_text(inspection_path)
        thermal_text = extract_text(thermal_path)

        ddr_content = generate_ddr(inspection_text, thermal_text)

    except Exception as e:
        ddr_content = f"""
DETAILED DIAGNOSTIC REPORT (DDR)

Error occurred during processing: {str(e)}

Basic fallback report generated.

1. Property Issue Summary
Dampness, leakage, and structural issues observed.

2. Area-wise Observations
Multiple areas affected including hall, bedroom, and bathroom.

3. Probable Root Cause
Water leakage and poor waterproofing.

4. Severity Assessment
Moderate

5. Recommended Actions
Waterproofing and plumbing repair required.

6. Additional Notes
System fallback activated.

7. Missing Information
Detailed inspection data not available.
"""

    # Generate PDF
    output_path = os.path.join(OUTPUT_FOLDER, "DDR_Report.pdf")
    create_pdf(ddr_content, output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)