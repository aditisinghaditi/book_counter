"""Book counting module using Google Gemini Vision API."""

import io
import os
import json

import google.generativeai as genai
from PIL import Image


def count_books(image_path: str = None, image_bytes: bytes = None) -> dict:
    """
    Count books in an image using Gemini Vision.

    Args:
        image_path: Path to the input image.
        image_bytes: Raw image bytes (alternative to path).

    Returns:
        Dictionary with 'count' and 'titles' (list of detected book titles).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    if image_bytes:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    elif image_path:
        img = Image.open(image_path).convert("RGB")
    else:
        raise ValueError("Provide either image_path or image_bytes")

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = """Look at this image of a book stack. Count the total number of individual books visible.

Instructions:
- Count each physical book separately, even if they look similar.
- Look at the spines/edges to identify individual books.
- If you can read titles or labels on the spines, list them.

Respond ONLY in this exact JSON format (no markdown, no code blocks):
{"count": <number>, "titles": ["title1", "title2", ...]}

If you cannot read some titles, use "Unreadable" as the title for those books.
"""

    response = model.generate_content([prompt, img])
    text = response.text.strip()

    # Remove markdown code blocks if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0].strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        result = {"count": 0, "titles": [], "raw_response": text}

    return result
