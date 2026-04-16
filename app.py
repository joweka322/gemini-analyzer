import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import base64

app = Flask(__name__)
CORS(app) # مهم جداً عشان يسمح لموقعك بالاتصال

# إعداد الجيمناي
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return "Server is running!"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        image_b64 = data.get('image')
        
        if not image_b64:
            return jsonify({"error": "No image provided"}), 400

        # تحويل الصورة
        image_data = base64.b64decode(image_b64)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([
            "حلل هذه الصورة بالتفصيل وباللغة العربية.",
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
