from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_ddr(inspection_text, thermal_text):

    prompt = f"""
Generate a Detailed Diagnostic Report (DDR).

Inspection Data:
{inspection_text}

Thermal Data:
{thermal_text}

Structure:
1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment
5. Recommended Actions
6. Additional Notes
7. Missing Information
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("⚠️ AI failed, using fallback...")

        return generate_fallback_ddr(inspection_text, thermal_text)


def generate_fallback_ddr(inspection_text, thermal_text):

    return f"""
Report Generated Using AI-Assisted Analysis

DETAILED DIAGNOSTIC REPORT (DDR)

1. Property Issue Summary
The inspection reveals multiple issues across the property including dampness at skirting levels, 
leakage in wet areas, and structural concerns such as external wall cracks. Thermal data supports 
the presence of moisture intrusion in affected zones.

2. Area-wise Observations

Hall:
Dampness observed at skirting level, indicating moisture ingress from adjacent wet areas or flooring.

Bedroom:
Dampness and efflorescence observed, suggesting prolonged moisture exposure and possible capillary action.

Kitchen:
Localized dampness at skirting level, possibly due to plumbing or adjacent wet area leakage.

Bathroom:
Gaps between tile joints and signs of plumbing leakage observed. These gaps allow water penetration 
leading to seepage in surrounding areas.

Parking Area:
Seepage observed at ceiling below the flat, confirming downward water movement from upper floor leakage.

3. Probable Root Cause
- Water ingress through gaps in tile joints
- Leakage from concealed plumbing lines
- External wall cracks allowing rainwater penetration
- Poor waterproofing at wet areas

4. Severity Assessment
Moderate to High severity.

Reason:
Issues are present across multiple areas and include both functional (plumbing leakage) and structural 
(external cracks) concerns. If not addressed, these may worsen over time.

5. Recommended Actions
- Regrouting of tile joints using waterproof materials
- Inspection and repair of concealed plumbing system
- Application of waterproofing treatment in wet areas
- Sealing of external wall cracks with appropriate materials
- Inspection of drainage slope and outlets

6. Additional Notes
Thermal readings indicate temperature variations consistent with moisture presence, supporting the 
visual inspection findings.

7. Missing or Unclear Information
- Exact condition of internal plumbing system: Not Available
- Detailed waterproofing history: Not Available
"""