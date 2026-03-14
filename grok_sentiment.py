import os
import requests
from dotenv import load_dotenv
from openai import OpenAI   # xAI is OpenAI-compatible

load_dotenv()

client = OpenAI(
    api_key=os.getenv('XAI_API_KEY'),
    base_url="https://api.x.ai/v1"
)

def get_grok_sentiment(symbol: str) -> dict:
    """Returns {'score': 0-100, 'reason': string}"""
    try:
        # Free public headlines (no API key needed)
        url = f"https://cryptopanic.com/api/v1/posts/?currencies={symbol.replace('/USD','')}&filter=hot&kind=news"
        resp = requests.get(url, timeout=8).json()
        headlines = [p['title'] for p in resp.get('results', [])[:12]]
        news_text = "\n".join(headlines)

        prompt = f"""
        You are a crypto sentiment expert.
        Analyze ONLY these recent headlines for {symbol}:

        {news_text}

        Score bullishness 0–100 (100 = extremely bullish).
        Respond in exactly this format:
        SCORE: 82
        REASON: One short sentence why.
        """

        completion = client.chat.completions.create(
            model="grok-4-1-1",   # your preferred model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3
        )

        text = completion.choices[0].message.content.strip()
        score_line = [line for line in text.splitlines() if "SCORE:" in line][0]
        score = int(score_line.split(":")[1].strip())

        reason = text.split("REASON:")[-1].strip() if "REASON:" in text else "No reason given"

        return {"score": score, "reason": reason}

    except Exception as e:
        return {"score": 50, "reason": f"Sentiment error: {str(e)[:100]}"}