from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import google.generativeai as genai
import base64
import os

app = Flask(__name__)
# تفعيل CORS بشكل يسمح لجميع المصادر بدون استثناء
CORS(app, resources={r"/*": {"origins": "*"}})

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    # معالجة طلب OPTIONS (الذي يسبق الفاتورة الحقيقية للتأكد من الأمان)
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    try:
        data = request.get_json()
        image_b64 = data.get('image')
        
        if not image_b64:
            return _corsify_actual_response(jsonify({"error": "No image"}), 400)

        image_data = base64.b64decode(image_b64)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content([
            "ما هذا الجهاز؟ اختر من: (لمبة، مروحة، شاشة، تكييف، ميكروويف، غسالة، ثلاجة). أجب بكلمة واحدة.",
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        return _corsify_actual_response(jsonify({"result": response.text.strip()}))
    except Exception as e:
        return _corsify_actual_response(jsonify({"error": str(e)}), 500)

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response, status=200):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status

# للمزامنة مع Vercel
def handler(event, context):
    return app(event, context)
