"""
╔══════════════════════════════════════════════════════════════╗
║         🌐 AI AGENT — CLOUD BACKEND (GEMINI)                ║
║         Railway.app da ishlaydi | 24/7 online               ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_KALIT = os.getenv("GEMINI_API_KEY", "")
if GEMINI_KALIT:
    genai.configure(api_key=GEMINI_KALIT)

app = Flask(__name__, static_folder=".")
CORS(app)

TIZIM_XABARI = """Sen o'zbek tilida professional AI yordamchisan.
Foydalanuvchi bilan do'stona suhbat qil.
Har qanday savol va buyruqqa o'zbek tilida ravon javob ber.
Qisqa va aniq bo'l."""

@app.route("/")
def index():
    """index_1.html ni ochadi"""
    return send_from_directory(".", "index_1.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data   = request.json or {}
        buyruq = data.get("buyruq", "").strip()
        rejim  = data.get("rejim", "suhbat")

        if not buyruq:
            return jsonify({"javob": "Buyruq bo'sh!"})

        if not GEMINI_KALIT:
            return jsonify({"javob": "❌ GEMINI_API_KEY sozlanmagan!"})

        # Rejimga qarab tizim xabari
        if rejim == "csharp":
            tizim = """Sen professional C# dasturchi va o'qituvchisan.
Savolga O'ZBEK tilida aniq va tushunarli javob ber.
Kod misollar keltir, izohlarni o'zbek tilida yoz."""
        elif rejim == "laptop":
            tizim = """Sen laptop boshqaruvchi AI agentsan.
Foydalanuvchi buyrug'ini o'zbek tilida tushuntir.
Agar buyruq faqat local kompyuterda bajarilishi kerak bo'lsa 
(masalan Telegram, ilovalar ochish), shuni ayt va tushuntir."""
        else:
            tizim = TIZIM_XABARI

        model  = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=tizim
        )
        javob  = model.generate_content(buyruq)
        return jsonify({"javob": javob.text})

    except Exception as e:
        return jsonify({"javob": f"❌ Xato: {str(e)}"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ishlayapti",
        "model":  "gemini-2.0-flash",
        "version": "cloud-1.0"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("=" * 50)
    print("   🌐 AI AGENT CLOUD BACKEND")
    print(f"   Port: {port}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=False)
