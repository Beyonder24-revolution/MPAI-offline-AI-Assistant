
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, render_template
from flask import Flask, jsonify, request, render_template
from core.ai_engine import OfflineAI
from core.app_mode import is_demo
from flask import Flask, request, jsonify, render_template
from flask import Flask, request, jsonify
from core.ai_engine import OfflineAI
from core.app_mode import is_demo   # <-- IMPORTANT

app = Flask(__name__)
ai = OfflineAI()

# ------------------------
# HOME ROUTE
# ------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# ------------------------
# CHAT ROUTE
# ------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "")
        reply = ai.ask(user_message)
        return jsonify({"reply": reply})
    except Exception as e:
        print("❌ CHAT ERROR:", e)
        return jsonify({"reply": "⚠️ Server error"}), 500


        user_message = data["message"]
        reply_text = ai.ask(user_message)

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("❌ CHAT ERROR:", e)
        return jsonify({"reply": "⚠️ Server error"}), 500


# ------------------------
# MAIN
# ------------------------
if __name__ == "__main__":
    print("🚀 Starting MPAI server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
