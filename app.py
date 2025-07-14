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
@app.route("/", methods=["GET", "POST"])
def index():
    plan = None  # or result, if you want to call it that
    if request.method == "POST":
        equation = request.form["equation"]
        prompt = f"Solve the following math equation. Show the answer clearly.\n\nEquation: {equation}"
        plan = get_ai_plan(prompt)
    return render_template("index.html", plan=plan)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))  # For local development only
