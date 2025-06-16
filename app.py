from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)  # loads variables from .env
app = Flask(__name__)

# Load environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Custom filter to split string
def split_filter(s, delimiter, maxsplit=-1):
    return s.split(delimiter, maxsplit)

# Register the custom filter with Jinja2
app.jinja_env.filters['split'] = split_filter

def create_prompt(user_info):
    return f"""
Act as a professional personal financial advisor. Provide a concise, structured, and personalized financial plan to reduce debt, optimize spending, and achieve the user's financial goal. Start directly with the financial plan, avoiding any introductory statements. Ensure all section titles and sentences begin with a capital letter, including numbered list items. Use clear headings and format the response for clarity.

User's financial information:
- Monthly income: ${user_info['income']}
- Rent/Mortgage: ${user_info['rent']}
- Total debt: ${user_info['debt']}
- Goal: {user_info['goal']}

Include the following sections:
- Financial Overview: List the user's provided financial details. Use proper capitalization
- Monthly Budget Breakdown: Suggest a monthly budget with percentages of income for each category, including housing, estimated utilities, savings, food, transportation, etc. . Use proper capitalization
- Debt Reduction Strategy: Provide actionable steps to reduce debt. Use proper capitalization (only include this section if debt > $0)
- Tips For Optimizing Spending: Offer practical spending tips. Use proper capitalization
- Savings And Emergency Fund: Advise on savings and emergency fund goals. Use proper capitalization
- Summary: Summarize the plan and next steps. Use proper capitalization
- Encouragement: Provide an encouraging message and support for the user. Use proper capitalization
"""

def get_ai_plan(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial planning assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_info = {
            "income": request.form["income"],
            "rent": request.form["rent"],
            "debt": request.form["debt"],
            "goal": request.form["goal"]
        }
        prompt = create_prompt(user_info)
        plan = get_ai_plan(prompt)
        return render_template("result.html", plan=plan, user_info=user_info)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
