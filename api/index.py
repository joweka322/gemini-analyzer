from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import google.generativeai as genai
import base64
import os

app = Flask(__name__)
# تفعيل السماح لكل المصادر لضمان عمل الـ Fetch من الموبايل
CORS(app, resources={r"/*": {"origins": "*"}})

# التأكد من وجود مفتاح الـ API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    # رد تلقائي بالموافقة على طلبات الـ preflight (الاستكشاف)
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "POST, OPTIONS")
        return response

    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return _create_response({"error": "No image data"}, 400)

        image_data = base64.b64decode(data['image'])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # تحليل الجهاز
        prompt = "ما هو هذا الجهاز الكهربائي؟ اختر كلمة واحدة فقط من: (لمبة، مروحة، شاشة، تكييف، ميكروويف، غسالة، ثلاجة)."
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
        
        return _create_response({"result": response.text.strip()})
    
    except Exception as e:
        return _create_response({"error": str(e)}, 500)

def _create_response(data, status=200):
    response = make_response(jsonify(data), status)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# خاص ببيئة Vercel
def handler(event, context):
    return app(event, context)
