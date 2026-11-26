import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Free-tier model fallback chain to handle rate limits gracefully
FREE_MODELS = [
    "nvidia/nemotron-3.5-lightning:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "inclusionai/ling-3.2-flash:free",
    "google/gemma-4-31b-it:free",
    "openrouter/free"
]


def call_openrouter(prompt: str, system_prompt: str) -> tuple[str, str]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing. Please add it to your .env file.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "NoteCraft AI"
    }

    last_error = ""
    for model in FREE_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4
        }
        try:
            res = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=45)
            if res.status_code == 200:
                data = res.json()
                content = data["choices"][0]["message"]["content"]
                return content, model
            last_error = f"{model} -> {res.status_code}"
        except Exception as e:
            last_error = f"{model} -> {str(e)}"

    raise RuntimeError(f"All free-tier models are currently unavailable. Last error: {last_error}")


def generate_study_pack(
    pdf_text: str = "",
    transcript: str = "",
    subject: str = "Engineering Subject",
    topic: str = ""
) -> tuple[str, str]:
    """Generates a structured Smart Study Pack from PDF notes and/or lecture audio transcripts."""
    system_prompt = (
        "You are NoteCraft AI, an exam-focused academic companion for engineering students (MSRIT). "
        "Be crisp, structured, and exam-oriented. Use clean Markdown with bullet points and code/formula blocks."
    )

    focus_line = f"Focus strictly on the topic: **{topic}**." if topic.strip() else "Cover all key concepts in the material."

    # Truncate context to stay within free-tier token limits
    pdf_chunk = pdf_text[:18000] if pdf_text else "None provided."
    audio_chunk = transcript[:12000] if transcript else "None provided."

    prompt = f"""Subject: {subject}
{focus_line}

=== CLASS NOTES / PDFs ===
{pdf_chunk}

=== LECTURE AUDIO TRANSCRIPT / TEACHER HINTS ===
{audio_chunk}

If the provided PDF/transcript does not match the requested Subject or Unit, start with a clear mismatch warning instead of making things up.
IF teacher hints are missing, highlight the high-weightage exam traps from the notes and pyq's and also from the topics that teacher put more effort in the class.   
Generate a clean exam revision pack with these exact sections:
### 1. Teacher Spotlight (Exam Hints & Traps)
Extract any emphasized topics, repeated derivations, edge cases, or exam warnings from the transcript (if no transcript is provided, highlight the top 3 high-weightage exam traps from the notes).

### 2. Structured Revision Notes
Concise, point-to-point breakdown of core concepts, definitions, and steps.

### 3. Key Formulas / Code / Derivations
Clean formulas or code snippets ready for exam writing.
Use ONLY $...$ for inline math and $$...$$ for block equations. Never use \[ \] or \( \).

### 4. 60-Second Quick Recap
5 crisp bullet points to skim right before entering the exam hall.
"""
    return call_openrouter(prompt, system_prompt)