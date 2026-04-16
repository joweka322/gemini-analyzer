from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import google.generativeai as genai
import base64
import os

app = Flask(__name__)
# السماح الكامل والمطلق لجميع النطاقات لتجنب "Failed to Fetch"
CORS(app, supports_credentials=True)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/analyze', methods=['POST', 'GET', 'OPTIONS'])
def analyze():
    # معالجة طلب الـ OPTIONS اللي المتصفح بيبعته للتأكد من الأمان
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    if request.method == 'GET':
        return jsonify({"status": "Server is running!"})
        
    try:
        data = request.get_json()
        image_b64 = data.get('image')
        
        if not image_b64:
            return jsonify({"error": "No image provided"}), 400

        image_data = base64.b64decode(image_b64)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # طلب التعرف على الجهاز
        response = model.generate_content([
            "ما هو هذا الجهاز الكهربائي؟ أجب بكلمة واحدة فقط من هذه القائمة: (لمبة، مروحة، شاشة، تكييف، ميكروويف، غسالة، ثلاجة).",
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        return jsonify({"result": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# مهم جداً لبيئة Vercel
def handler(event, context):
    return app(event, context)
