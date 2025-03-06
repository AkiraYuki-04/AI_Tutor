from flask import Blueprint, request, jsonify
import wikipediaapi

# Define Blueprint
fetch_history = Blueprint("fetch_history", __name__)  

# Wikipedia API setup
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="AI-History-Tutor/1.0 (Contact: your-email@example.com)"
)

@fetch_history.route("/", methods=["GET"])  #route setup
def get_historical_info():
    topic = request.args.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    page = wiki.page(topic)
    if not page.exists():
        return jsonify({"error": "Topic not found"}), 404

    return jsonify({
        "title": page.title,
        "summary": page.summary[:1000],  # Limit text length
        "source": page.fullurl  # Wikipedia source link
    })

