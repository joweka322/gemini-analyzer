from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import base64
import os

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        image_b64 = data.get('image')
        image_data = base64.b64decode(image_b64)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([
            "حلل هذه الصورة بالتفصيل وباللغة العربية.",
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# مهم جداً لـ Vercel
def handler(event, context):
    return app(event, context)
