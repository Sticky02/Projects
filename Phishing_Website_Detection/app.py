from flask import Flask, request, jsonify, render_template
from model_utils import predict_hybrid

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_url_legitimacy():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    prediction = predict_hybrid(url)
    
    return jsonify({"url": url, "prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)
