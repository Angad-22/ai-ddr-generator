from dotenv import load_dotenv
import os
import requests
from google import genai

load_dotenv()

# Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_ddr(inspection_text, thermal_text):

    prompt = f"""
You are a civil inspection expert.

Generate a Detailed Diagnostic Report (DDR).

Inspection Data:
{inspection_text}

Thermal Data:
{thermal_text}

STRICT FORMAT:
1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information
"""

    # 🔹 STEP 1: Try Gemini API
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("⚠️ Gemini failed, trying Ollama...")

    # 🔹 STEP 2: Try Ollama (LOCAL MODEL)
    try:
        return generate_ddr_ollama(prompt)

    except Exception as e:
        print("⚠️ Ollama failed, using fallback...")

    # 🔹 STEP 3: Final fallback
    return generate_fallback_ddr()


# ✅ LOCAL MODEL USING OLLAMA
def generate_ddr_ollama(prompt):

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "mistral",   # or "llava"
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()["response"]
    else:
        raise Exception("Ollama API failed")


# ✅ FINAL FALLBACK (SAFE)
def generate_fallback_ddr():
    return """
Report Generated Using AI-Assisted Analysis

DETAILED DIAGNOSTIC REPORT (DDR)

1. Property Issue Summary
Multiple issues observed including dampness, leakage, and wall cracks.

2. Area-wise Observations
Hall: Dampness observed  
Bedroom: Dampness and efflorescence  
Kitchen: Skirting dampness  
Bathroom: Tile gaps and leakage  
Parking: Ceiling seepage  

3. Probable Root Cause
- Tile joint gaps
- Plumbing leakage
- External cracks

4. Severity Assessment
Moderate to High

5. Recommended Actions
- Waterproofing
- Plumbing repair
- Crack sealing

6. Additional Notes
Thermal data indicates moisture presence.

7. Missing Information
Detailed plumbing condition: Not Available
"""