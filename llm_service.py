import os
import json
from openai import OpenAI

# --- LLM client (Nebius) ---
client = OpenAI(
    api_key=os.getenv("NEBIUS_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

MODEL = os.getenv("MODEL")


def summarize_text(text: str):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an API that returns only valid JSON."
            },
            {
    "role": "user",
    "content": f"""
Summarize this GitHub repository.

Return ONLY JSON in this format:

{{
  "summary": "1-2 sentences",
  "technologies": ["tech1", "tech2"],
  "structure": "short description of project structure in 1 sentence"
}}

Rules:
- structure must be a short TEXT, not an object
- technologies: max 5 items
- no extra fields

Repository context:
{text}
"""
}
        ]
    )

    content = response.choices[0].message.content

    try:
        result = json.loads(content)
        structure = result.get("structure", "")
        if isinstance(structure, dict):
            structure = json.dumps(structure)

        return {
          "summary": result.get("summary", ""),
          "technologies": result.get("technologies", []),
          "structure": structure
        }

    except Exception:
        return {
            "summary": "Failed to parse LLM output",
            "technologies": [],
            "structure": "Unknown"
        }
