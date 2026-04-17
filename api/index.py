import os
import base64
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# تفعيل CORS بشكل كامل ومفتوح لكل المصادر
CORS(app, resources={r"/*": {"origins": "*"}})

# تهيئة Gemini باستخدام مفتاحك المخفي في Vercel
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    # رد فوري على طلبات المتصفح الاستكشافية (Preflight)
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "POST, OPTIONS")
        return response

    try:
        # استلام البيانات
        data = request.get_json()
        if not data or 'image' not in data:
            return _make_cors_response({"error": "No image provided"}, 400)

        # تحويل الصورة من Base64
        image_data = base64.b64decode(data['image'])
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # تحليل الصورة بكلمة واحدة فقط
        prompt = "ما هو هذا الجهاز الكهربائي؟ أجب بكلمة واحدة فقط من هذه القائمة: (لمبة، مروحة، شاشة، تكييف، ميكروويف، غسالة، ثلاجة)."
        
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        result = response.text.strip()
        return _make_cors_response({"result": result})

    except Exception as e:
        return _make_cors_response({"error": str(e)}, 500)

def _make_cors_response(data, status=200):
    response = make_response(jsonify(data), status)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# متطلب لـ Vercel Serverless
def handler(event, context):
    return app(event, context)
