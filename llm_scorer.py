import json
import config

def score_chunk_with_llm(chunk_text):
    """Sends transcript chunk to Gemini to rate viral hook potential (1-10)."""
    if not config.GEMINI_API_KEY:
        matches = sum(1 for kw in config.FALLBACK_KEYWORDS if kw in chunk_text.lower())
        score = min(10, matches * 2.5)
        return score, "Keyword-based fallback evaluation"

    try:
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        Rate the viral hook potential of this clip transcript on a scale from 1 to 10.
        Consider storytelling quality, emotional intensity, humor, or strong takeaways.

        Transcript: "{chunk_text}"

        Respond strictly in valid JSON format:
        {{"score": <number_1_to_10>, "reasoning": "<short_explanation>"}}
        """

        response = model.generate_content(prompt)
        data = json.loads(response.text.strip().strip("```json").strip("```"))
        return float(data.get("score", 5.0)), data.get("reasoning", "")

    except Exception as e:
        print(f"[LLM Scorer] Evaluation warning: {e}. Defaulting score.")
        return 5.0, "Default baseline score"
