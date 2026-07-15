import os
import google.generativeai as genai
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from extensions import db
from models import Video, Subtitle

ai_bp = Blueprint("ai", __name__)

# Use the latest stable models that work with current API
MODELS_TO_TRY = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
]

if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=Config.GEMINI_API_KEY)
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(f"✅ Available Gemini models: {available_models}")
    except Exception as e:
        print(f"⚠️ Could not list models: {e}")
        available_models = []
else:
    available_models = []


def get_model():
    """Get a working Gemini model, trying the latest first."""
    for model_name in MODELS_TO_TRY:
        try:
            return genai.GenerativeModel(model_name), model_name
        except Exception:
            continue
    return None, None


def generate_ai_response(prompt):
    """Generic Gemini caller with graceful fallback."""
    if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return (
            "⚠️ AI service is not configured.\n\n"
            "Please set your GEMINI_API_KEY in backend/.env to enable AI features.\n\n"
            "Get a free key at: https://aistudio.google.com/app/apikey"
        )
    model, model_name = get_model()
    if not model:
        return "❌ No working Gemini model found. Check your API key and internet connection."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ AI service error: {str(e)}\n\nModel used: {model_name}"


@ai_bp.route("/summarize", methods=["POST"])
@jwt_required()
def summarize():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    video_id = data.get("video_id")

    if video_id and not text:
        subtitles = Subtitle.query.filter_by(video_id=video_id).all()
        if subtitles:
            text = " ".join(s.content for s in subtitles)
        else:
            video = Video.query.get(video_id)
            if video:
                text = video.description or video.title

    if not text:
        return jsonify({"error": "No text to summarize"}), 400

    prompt = (
        "Please provide a clear, structured summary of the following educational content. "
        "Use bullet points and key takeaways. Keep it concise (around 200-300 words):\n\n"
        f"{text}"
    )
    summary = generate_ai_response(prompt)
    return jsonify({"summary": summary, "source_length": len(text)})


@ai_bp.route("/keypoints", methods=["POST"])
@jwt_required()
def keypoints():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    video_id = data.get("video_id")

    if video_id and not text:
        subtitles = Subtitle.query.filter_by(video_id=video_id).all()
        if subtitles:
            text = " ".join(s.content for s in subtitles)

    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = (
        "Extract the top 7-10 key learning points from this educational content. "
        "Format as a numbered list with short, clear statements:\n\n"
        f"{text}"
    )
    points = generate_ai_response(prompt)
    return jsonify({"keypoints": points})


@ai_bp.route("/explain", methods=["POST"])
@jwt_required()
def explain():
    data = request.get_json() or {}
    topic = data.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Topic required"}), 400

    prompt = (
        f"Explain the following concept in simple terms for a student. "
        f"Include a short definition, an analogy, and 2-3 examples:\n\nTopic: {topic}"
    )
    explanation = generate_ai_response(prompt)
    return jsonify({"explanation": explanation})


@ai_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    context = data.get("context", "")
    if not message:
        return jsonify({"error": "Message required"}), 400

    prompt = (
        f"You are a helpful teaching assistant for an online learning platform. "
        f"Context: {context}\n\nStudent: {message}\n\nAssistant:"
    )
    reply = generate_ai_response(prompt)
    return jsonify({"reply": reply})


@ai_bp.route("/generate-quiz", methods=["POST"])
@jwt_required()
def generate_quiz():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    video_id = data.get("video_id")
    num_questions = int(data.get("num_questions", 5))

    if video_id and not text:
        subtitles = Subtitle.query.filter_by(video_id=video_id).all()
        if subtitles:
            text = " ".join(s.content for s in subtitles)

    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = (
        f"Generate {num_questions} multiple-choice questions (4 options each) "
        f"from the following content. Return ONLY valid JSON in this exact format:\n"
        f'{{"questions":[{{"question":"...","options":["A","B","C","D"],"answer":0}}]}}\n\n'
        f"Content:\n{text}"
    )
    raw = generate_ai_response(prompt)
    return jsonify({"raw": raw})


@ai_bp.route("/models", methods=["GET"])
@jwt_required()
def list_models():
    """Debug endpoint to list available models."""
    if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return jsonify({"error": "API key not configured"}), 400
    try:
        models = genai.list_models()
        return jsonify({
            "models": [
                {
                    "name": m.name,
                    "supported_methods": list(m.supported_generation_methods)
                }
                for m in models
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
