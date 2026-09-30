from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = FastAPI(title="PocketSmart AI")

app.mount("/static", StaticFiles(directory="static"), name="static")


class RecommendationRequest(BaseModel):
    planner: str
    budget: float
    details: str = ""


def fallback_recommendation(data: RecommendationRequest):
    budget = data.budget
    planner = data.planner.lower()

    if planner == "home":
        return f"""
HOME INTERIOR BUDGET PLAN

Total Budget: ₹{budget:,.0f}

Suggested allocation:
• Lighting: 15%
• Ceiling fan: 15%
• Furniture: 35%
• Storage: 20%
• Decoration: 15%

Sample plan:
1. LED lights – ₹{budget * 0.08:,.0f}
2. Ceiling fan – ₹{budget * 0.12:,.0f}
3. Basic furniture – ₹{budget * 0.35:,.0f}
4. Storage solutions – ₹{budget * 0.20:,.0f}
5. Decoration – ₹{budget * 0.15:,.0f}

Tip: Keep around 5–10% as a buffer for unexpected expenses.
"""

    if planner == "party":
        return f"""
PARTY BUDGET PLAN

Total Budget: ₹{budget:,.0f}

Suggested allocation:
• Food & Catering: 45%
• Decoration: 20%
• Entertainment: 20%
• Venue / Other expenses: 15%

Estimated allocation:
• Catering – ₹{budget * 0.45:,.0f}
• Decoration – ₹{budget * 0.20:,.0f}
• Entertainment – ₹{budget * 0.20:,.0f}
• Other expenses – ₹{budget * 0.15:,.0f}

Details provided:
{data.details}
"""

    return f"""
JEWELRY BUDGET PLAN

Total Budget: ₹{budget:,.0f}

Suggested allocation:
• Main jewelry: 60%
• Matching accessory: 20%
• Earrings / small accessories: 15%
• Buffer: 5%

Estimated allocation:
• Main jewelry – ₹{budget * 0.60:,.0f}
• Matching accessory – ₹{budget * 0.20:,.0f}
• Earrings / accessories – ₹{budget * 0.15:,.0f}
• Buffer – ₹{budget * 0.05:,.0f}

Occasion / Style:
{data.details}
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
async def health():
    return {"status": "PocketSmart AI is running"}


@app.post("/api/recommend")
async def recommend(data: RecommendationRequest):

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        return {
            "success": True,
            "source": "PocketSmart AI Smart Fallback",
            "recommendation": fallback_recommendation(data)
        }

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are PocketSmart AI, a smart budget planning assistant.

Planner type: {data.planner}
Total budget: ₹{data.budget:,.0f}
User details: {data.details}

Create a practical budget recommendation.

Requirements:
- Respect the user's total budget.
- Give clear percentage allocation.
- Give approximate amounts in INR.
- Suggest useful categories.
- Keep recommendations realistic.
- Mention that prices can vary.
- Do not claim live prices unless verified.
- Use simple headings and bullet points.
- Do not exceed the user's budget.
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        text = response.text if response.text else fallback_recommendation(data)

        return {
            "success": True,
            "source": "Google Gemini",
            "recommendation": text
        }

    except Exception as e:
        return {
            "success": True,
            "source": "PocketSmart AI Fallback",
            "recommendation": fallback_recommendation(data),
            "note": "Gemini is temporarily unavailable, so the built-in budget engine generated this recommendation."
        }
