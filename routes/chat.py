from flask import Blueprint, request, jsonify
import google.generativeai as genai # Google Gemini AI SDK
import wikipediaapi
from config import GOOGLE_AI_API_KEY  # Store your Gemini API key in config.py
from flask_cors import CORS

# ✅ Configure Google Gemini API
genai.configure(api_key=GOOGLE_AI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Use a faster Gemini model

# Create Blueprint for chat routes
ai_chat = Blueprint("ai_chat", __name__)
CORS(ai_chat) 

# Wikipedia setup
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="AI-History-Tutor/1.0 (Contact: your-email@example.com)"
)

@ai_chat.route("/", methods=["POST"])
def get_ai_response():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Step 1: Fetch Wikipedia Summary
    page = wiki.page(user_query)
    wiki_summary = page.summary[:1000] if page.exists() else "No Wikipedia data found."

    # Step 2: Use Google Gemini AI to Generate a Response
    try:
        response = model.generate_content([
            "You are an expert AI history tutor. Provide detailed, engaging, and informative responses.",
            f"Tell me about {user_query} in detail.",
            wiki_summary,
            "Expand on this with more historical insights and important facts."
        ])

        ai_response = response.text  #  Extract response from Gemini AI

        return jsonify({
            "query": user_query,
            "wiki_summary": wiki_summary,
            "ai_response": ai_response
        })

    except Exception as e:
        print(f"Error occurred: {e}")  # Debugging
        return jsonify({"error": str(e)}), 500
