import os
from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import base64
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro-vision')

def generate_compliment(image_data):
    try:
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        response = model.generate_content([
            'Give me a kind and specific compliment about this image. Keep it concise and friendly.',
            image
        ])
        return response.text
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    image_data = request.json.get('image')
    if not image_data:
        return jsonify({'error': 'No image provided'}), 400
    compliment = generate_compliment(image_data)
    return jsonify({'compliment': compliment})

if __name__ == '__main__':
    app.run(debug=True)