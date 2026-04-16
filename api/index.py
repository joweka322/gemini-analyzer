from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import base64
import os

app = Flask(__name__)
# السماح الكامل لأي موقع بالاتصال (حل مشكلة فشل الاتصال)
CORS(app, resources={r"/*": {"origins": "*"}})

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/analyze', methods=['POST', 'GET', 'OPTIONS'])
def analyze():
    if request.method == 'GET':
        return jsonify({"status": "Server is running!"})
        
    try:
        data = request.get_json()
        image_b64 = data.get('image')
        
        if not image_b64:
            return jsonify({"error": "No image"}), 400

        image_data = base64.b64decode(image_b64)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # طلب التعرف على الجهاز
        response = model.generate_content([
            "ما هو هذا الجهاز الكهربائي؟ أجب بكلمة واحدة فقط من القائمة: (لمبة، مروحة، شاشة، تكييف، ميكروويف، غسالة، ثلاجة).",
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        return jsonify({"result": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(event, context):
    return app(event, context)
