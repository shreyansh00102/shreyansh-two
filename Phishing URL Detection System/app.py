"""
=============================================================
  FLASK APP — Main Backend Server
=============================================================
  Ye file Flask server chalati hai jo:
  1. Homepage (UI) serve karti hai
  2. /predict API pe URL le ke result deti hai
  
  Run karo:  python app.py
  Browser:   http://localhost:5000
=============================================================
"""

import os
import json
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from feature_extractor import extract_features, get_reasons

# ---- Flask App Create Karo ----
app = Flask(__name__)
CORS(app)  # Cross-Origin requests allow karo

# ---- Model Load Karo ----
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'phishing_model.pkl')
MODEL_INFO_PATH = os.path.join(os.path.dirname(__file__), 'model', 'model_info.json')

model = None
model_info = None

def load_model():
    """Trained model load karo. Agar nahi mila toh error do."""
    global model, model_info
    
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("[+] Model loaded successfully!")
    else:
        print("[!] Model file not found! Pehle train karo:")
        print("   python model/train_model.py")
    
    if os.path.exists(MODEL_INFO_PATH):
        with open(MODEL_INFO_PATH, 'r') as f:
            model_info = json.load(f)
        print(f"[*] Model accuracy: {model_info.get('accuracy', 0) * 100:.1f}%")


# ==============================================================
#  ROUTE 1: Homepage — UI Serve Karo
# ==============================================================
@app.route('/')
def home():
    """Main page serve karo."""
    return render_template('index.html')


# ==============================================================
#  ROUTE 2: /predict — URL Check Karo
# ==============================================================
@app.route('/predict', methods=['POST'])
def predict():
    """
    URL le ke predict karo — Safe ya Phishing?
    
    Input (JSON):
        { "url": "https://example.com" }
    
    Output (JSON):
        {
            "result": "safe" or "phishing",
            "confidence": 95.5,
            "reasons": [...],
            "features": {...}
        }
    """
    try:
        # Step 1: URL lo request se
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                "error": "URL provide karo!",
                "result": None
            }), 400
        
        # URL mein http/https add karo agar nahi hai
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Step 2: Features nikalo
        features = extract_features(url)
        features_array = np.array([features])
        
        # Step 3: Reasons nikalo (kyun suspicious hai)
        reasons = get_reasons(url)
        
        # Step 4: Model se predict karo
        if model is not None:
            prediction = model.predict(features_array)[0]
            probabilities = model.predict_proba(features_array)[0]
            
            # Confidence score
            confidence = float(max(probabilities) * 100)
            
            # Result
            result = "phishing" if prediction == 1 else "safe"
            
            # Phishing probability
            phishing_prob = float(probabilities[1] * 100)
            safe_prob = float(probabilities[0] * 100)
        else:
            # Agar model load nahi hua toh rule-based fallback
            result, confidence, phishing_prob, safe_prob = rule_based_check(features, reasons)
        
        # Step 5: Response bhejo
        response = {
            "url": url,
            "result": result,
            "confidence": round(confidence, 1),
            "phishing_probability": round(phishing_prob, 1),
            "safe_probability": round(safe_prob, 1),
            "reasons": reasons,
            "features": dict(zip(
                ['url_length', 'has_ip', 'num_dots', 'has_at', 
                 'has_double_slash', 'has_dash', 'num_subdomains',
                 'is_https', 'url_depth', 'uses_shortener',
                 'num_special_chars', 'domain_length', 'num_digits',
                 'has_suspicious_words', 'has_encoding'],
                features
            )),
            "model_accuracy": model_info.get('accuracy', 0) * 100 if model_info else None
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "error": f"Error: {str(e)}",
            "result": None
        }), 500


def rule_based_check(features, reasons):
    """
    Fallback: Agar ML model load nahi hua toh 
    rule-based checking karo.
    """
    score = 0
    total_checks = 15
    
    # Feature thresholds
    if features[0] > 75: score += 2    # URL too long
    elif features[0] > 54: score += 1
    if features[1] == 1: score += 3     # Has IP
    if features[2] > 4: score += 2      # Too many dots
    if features[3] == 1: score += 3     # Has @
    if features[4] == 1: score += 2     # Double slash
    if features[5] == 1: score += 1     # Has dash
    if features[6] > 2: score += 2      # Too many subdomains
    if features[7] == 0: score += 1     # No HTTPS
    if features[8] > 3: score += 1      # Deep URL
    if features[9] == 1: score += 2     # Shortener
    if features[10] > 3: score += 1     # Special chars
    if features[11] > 25: score += 1    # Long domain
    if features[12] > 3: score += 2     # Digits in domain
    if features[13] == 1: score += 1    # Suspicious words
    if features[14] == 1: score += 1    # URL encoding
    
    max_score = 23
    phishing_prob = (score / max_score) * 100
    safe_prob = 100 - phishing_prob
    
    if phishing_prob > 40:
        result = "phishing"
        confidence = phishing_prob
    else:
        result = "safe"
        confidence = safe_prob
    
    return result, confidence, phishing_prob, safe_prob


# ==============================================================
#  ROUTE 3: /model-info — Model Ki Info
# ==============================================================
@app.route('/model-info')
def get_model_info():
    """Model ki info return karo (accuracy, features etc.)."""
    if model_info:
        return jsonify(model_info)
    return jsonify({"error": "Model info not available"})


# ==============================================================
#  SERVER START
# ==============================================================
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("[*] PHISHING URL DETECTION SYSTEM")
    print("=" * 60)
    
    load_model()
    
    print("\n[*] Server start ho raha hai...")
    print("[*] Browser mein kholo: http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=5000)
