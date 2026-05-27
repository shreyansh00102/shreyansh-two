"""
=============================================================
  MODEL TRAINING SCRIPT — Kaggle Dataset Integrated
=============================================================
  Ye script:
  1. Kaggle Phishing Dataset (58,645 URLs) load karta hai
  2. Apne sample URLs bhi add karta hai (100 URLs)
  3. Features select karke Random Forest model train karta hai
  4. Model ko .pkl file mein save karta hai
  
  Dataset: GregaVrbancic/Phishing-Dataset (GitHub/Kaggle)
  Total Data: ~58,745 URLs (Kaggle 58,645 + Sample 100)
  
  Run karo:  python model/train_model.py
=============================================================
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Parent folder ko path mein add karo (feature_extractor import ke liye)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from feature_extractor import extract_features, get_feature_names


# =============================================================
#  KAGGLE DATASET KA PATH
# =============================================================
DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset_small.csv')


# =============================================================
#  SAMPLE URLs — Apne manually added URLs (backup + supplement)
# =============================================================
# Label: 0 = Safe (Legitimate), 1 = Phishing

SAMPLE_URLS = [
    # ========== SAFE URLs (Label: 0) ==========
    ("https://www.google.com", 0),
    ("https://www.youtube.com", 0),
    ("https://www.facebook.com", 0),
    ("https://www.amazon.com", 0),
    ("https://www.wikipedia.org", 0),
    ("https://www.twitter.com", 0),
    ("https://www.instagram.com", 0),
    ("https://www.linkedin.com", 0),
    ("https://www.reddit.com", 0),
    ("https://www.github.com", 0),
    ("https://www.netflix.com", 0),
    ("https://www.microsoft.com", 0),
    ("https://www.apple.com", 0),
    ("https://www.stackoverflow.com", 0),
    ("https://www.medium.com", 0),
    ("https://www.spotify.com", 0),
    ("https://www.whatsapp.com", 0),
    ("https://www.zoom.us", 0),
    ("https://www.dropbox.com", 0),
    ("https://www.slack.com", 0),
    ("https://www.adobe.com", 0),
    ("https://www.cloudflare.com", 0),
    ("https://www.shopify.com", 0),
    ("https://www.stripe.com", 0),
    ("https://www.notion.so", 0),
    ("https://www.figma.com", 0),
    ("https://www.canva.com", 0),
    ("https://www.trello.com", 0),
    ("https://www.atlassian.com", 0),
    ("https://www.salesforce.com", 0),
    ("https://mail.google.com/mail/inbox", 0),
    ("https://docs.google.com/document/d/abc123", 0),
    ("https://www.bbc.com/news", 0),
    ("https://www.nytimes.com/section/world", 0),
    ("https://www.cnn.com/politics", 0),
    ("https://www.flipkart.com", 0),
    ("https://www.myntra.com", 0),
    ("https://www.zomato.com", 0),
    ("https://www.swiggy.com", 0),
    ("https://www.paytm.com", 0),
    ("https://www.phonepe.com", 0),
    ("https://www.razorpay.com", 0),
    ("https://www.irctc.co.in", 0),
    ("https://www.nptel.ac.in", 0),
    ("https://www.geeksforgeeks.org", 0),
    ("https://www.hackerrank.com", 0),
    ("https://www.leetcode.com", 0),
    ("https://www.coursera.org", 0),
    ("https://www.udemy.com", 0),
    ("https://www.edx.org", 0),
    
    # ========== PHISHING URLs (Label: 1) ==========
    ("http://192.168.1.1/login/secure/bank/verify", 1),
    ("http://192.168.0.1/paypal/login.php", 1),
    ("http://10.0.0.1/account/verify/update", 1),
    ("http://172.16.0.1/signin/credential/update", 1),
    ("http://g00gle-secure-login.tk/verify?user=admin", 1),
    ("http://faceb00k-login.ml/signin.html", 1),
    ("http://amaz0n-verify.cf/account/login", 1),
    ("http://netfl1x-update.ga/billing/verify", 1),
    ("http://paypa1-secure.tk/login/confirm", 1),
    ("http://apple-id-verify.ml/account/suspend", 1),
    ("http://microsoft-alert.cf/login/verify/password", 1),
    ("http://bank-secure-login.tk/account/update", 1),
    ("http://instagram-verify.ga/login/confirm", 1),
    ("http://linkedin-secure.ml/signin/verify", 1),
    ("http://twitter-alert.cf/account/suspend/verify", 1),
    ("http://google.com@evil-site.com/login", 1),
    ("http://facebook.com@malicious.tk/signin", 1),
    ("http://amazon.com@phishing.ml/verify", 1),
    ("http://bit.ly/3xFakeLink", 1),
    ("http://tinyurl.com/SuspiciousPage", 1),
    ("http://secure-bank-login-verify-account.tk/update", 1),
    ("http://www.a.b.c.d.e.f.evil.com/login", 1),
    ("http://login-verify-secure-bank-account.ml/update/password", 1),
    ("http://credential-update-verify.cf/login/bank", 1),
    ("http://account-alert-suspend.ga/verify/login", 1),
    ("http://paytm-secure-login.tk/wallet/verify", 1),
    ("http://phonepe-verify.ml/account/update", 1),
    ("http://sbi-online-login.tk/netbanking/verify", 1),
    ("http://hdfc-secure.cf/login/password/update", 1),
    ("http://icici-alert.ga/account/suspend/verify", 1),
    ("http://flipkart-offer.tk/login/verify/prize", 1),
    ("http://amazon-prize-winner.ml/claim/verify/login", 1),
    ("http://whatsapp-gold.cf/download/verify/login", 1),
    ("http://covid-relief-fund.tk/apply/verify/account", 1),
    ("http://urgent-bank-alert.ml/verify/login/password", 1),
    ("http://192.168.1.100/phishing/login/fake-page.html", 1),
    ("http://secure.login.verify.account.update.evil.tk/confirm", 1),
    ("http://a1b2c3d4.tk/login/verify", 1),
    ("http://xn--googl-ysa.com/signin", 1),
    ("http://update-your-password-now.ml/bank/login", 1),
    ("http://free-iphone-winner.tk/claim/login/verify", 1),
    ("http://account-locked-verify.cf/login/update/alert", 1),
    ("http://verify-your-email-now.ga/login/confirm/urgent", 1),
    ("http://reward-claim-verify.tk/login/account/prize", 1),
    ("http://security-alert-login.ml/verify/password/update", 1),
    ("http://click-here-verify-now.cf/login/urgent", 1),
    ("http://limited-offer-claim.ga/login/verify/prize", 1),
    ("http://suspicious-link.tk/redirect//evil.com/login", 1),
    ("http://login%40verify.tk/account/update", 1),
    ("http://secure%2Flogin.ml/verify/password", 1),
]


# =============================================================
#  KAGGLE DATASET FEATURES → HUMARI FEATURES MAPPING
# =============================================================
# 
# Kaggle dataset mein 112 features hain. Humari 15 features ke 
# liye relevant columns select karenge.
#
# Mapping:
#   Our Feature          ← Kaggle Column
#   ──────────────────────────────────────
#   url_length           ← length_url
#   has_ip_address       ← domain_in_ip
#   num_dots             ← qty_dot_url
#   has_at_symbol        ← qty_at_url (>0 → 1)
#   has_double_slash     ← qty_slash_url (>2 → 1)
#   has_dash_in_domain   ← qty_hyphen_domain (>0 → 1)
#   num_subdomains       ← qty_dot_domain
#   is_https             ← tls_ssl_certificate
#   url_depth            ← qty_slash_directory
#   uses_shortener       ← url_shortened
#   num_special_chars    ← qty_percent_url + qty_equal_url + qty_and_url
#   domain_length        ← domain_length
#   num_digits_in_domain ← derived (approximation)
#   has_suspicious_words ← derived (approximation)
#   has_url_encoding     ← qty_percent_url (>0 → 1)
# =============================================================


def load_kaggle_dataset():
    """
    Kaggle dataset load karo aur humari 15 features mein convert karo.
    
    Returns:
        X_kaggle: numpy array of features
        y_kaggle: numpy array of labels
    """
    print("\n  [*] Loading Kaggle dataset from:", DATASET_PATH)
    
    if not os.path.exists(DATASET_PATH):
        print("  [!] Kaggle dataset not found! Downloading...")
        try:
            import urllib.request
            url = "https://raw.githubusercontent.com/GregaVrbancic/Phishing-Dataset/master/dataset_small.csv"
            urllib.request.urlretrieve(url, DATASET_PATH)
            print("  [+] Dataset downloaded successfully!")
        except Exception as e:
            print(f"  [!] Download failed: {e}")
            print("  [!] Continuing with sample data only...")
            return None, None
    
    # CSV load karo
    df = pd.read_csv(DATASET_PATH)
    print(f"  [+] Kaggle dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # ── Features mapping ──
    # Har Kaggle column ko humari feature mein convert karo
    
    X_mapped = pd.DataFrame()
    
    # 1. url_length ← length_url
    X_mapped['url_length'] = df['length_url']
    
    # 2. has_ip_address ← domain_in_ip (1 = has IP)
    X_mapped['has_ip_address'] = df['domain_in_ip'].apply(lambda x: 1 if x == 1 else 0)
    
    # 3. num_dots ← qty_dot_url
    X_mapped['num_dots'] = df['qty_dot_url']
    
    # 4. has_at_symbol ← qty_at_url > 0
    X_mapped['has_at_symbol'] = (df['qty_at_url'] > 0).astype(int)
    
    # 5. has_double_slash ← qty_slash_url > 2 (normal URLs have 2 slashes: http://)
    X_mapped['has_double_slash'] = (df['qty_slash_url'] > 4).astype(int)
    
    # 6. has_dash_in_domain ← qty_hyphen_domain > 0
    X_mapped['has_dash_in_domain'] = (df['qty_hyphen_domain'] > 0).astype(int)
    
    # 7. num_subdomains ← qty_dot_domain (approx: dots in domain = subdomains)
    X_mapped['num_subdomains'] = df['qty_dot_domain'].clip(lower=0)
    
    # 8. is_https ← tls_ssl_certificate (1 = has SSL)
    X_mapped['is_https'] = df['tls_ssl_certificate'].apply(lambda x: 1 if x == 1 else 0)
    
    # 9. url_depth ← qty_slash_directory
    X_mapped['url_depth'] = df['qty_slash_directory'].clip(lower=0)
    
    # 10. uses_shortener ← url_shortened
    X_mapped['uses_shortener'] = df['url_shortened'].apply(lambda x: 1 if x == 1 else 0)
    
    # 11. num_special_chars ← qty_percent_url + qty_equal_url + qty_and_url + qty_questionmark_url
    X_mapped['num_special_chars'] = (
        df['qty_percent_url'].clip(lower=0) + 
        df['qty_equal_url'].clip(lower=0) + 
        df['qty_and_url'].clip(lower=0) +
        df['qty_questionmark_url'].clip(lower=0)
    )
    
    # 12. domain_length ← domain_length
    X_mapped['domain_length'] = df['domain_length']
    
    # 13. num_digits_in_domain ← approximate from domain features
    # Use dollar + hashtag + asterisk count as proxy for unusual chars
    X_mapped['num_digits_in_domain'] = (
        df['qty_dollar_domain'].clip(lower=0) + 
        df['qty_underline_domain'].clip(lower=0)
    ).clip(upper=10)
    
    # 14. has_suspicious_words ← derived: long directory + deep path = suspicious
    # Approximate: if directory is very long, likely has suspicious path
    X_mapped['has_suspicious_words'] = (df['directory_length'] > 50).astype(int)
    
    # 15. has_url_encoding ← qty_percent_url > 0
    X_mapped['has_url_encoding'] = (df['qty_percent_url'] > 0).astype(int)
    
    # Replace any NaN/infinite values
    X_mapped = X_mapped.fillna(0)
    X_mapped = X_mapped.replace([np.inf, -np.inf], 0)
    
    X_kaggle = X_mapped.values.astype(float)
    y_kaggle = df['phishing'].values
    
    print(f"  [+] Features mapped: {X_mapped.shape[1]} features per URL")
    print(f"  [+] Safe URLs in Kaggle: {sum(y_kaggle == 0)}")
    print(f"  [+] Phishing URLs in Kaggle: {sum(y_kaggle == 1)}")
    
    return X_kaggle, y_kaggle


def load_sample_urls():
    """
    Apne manually defined sample URLs se features nikalo.
    """
    print("\n  [*] Processing sample URLs...")
    
    X = []
    y = []
    
    for url, label in SAMPLE_URLS:
        try:
            features = extract_features(url)
            X.append(features)
            y.append(label)
        except Exception as e:
            print(f"  [!] Skip: {url} - Error: {e}")
    
    X = np.array(X, dtype=float)
    y = np.array(y)
    
    print(f"  [+] Sample URLs processed: {len(X)}")
    print(f"  [+] Safe: {sum(y == 0)}, Phishing: {sum(y == 1)}")
    
    return X, y


def train_model():
    """Model train karne ka main function — with Kaggle dataset."""
    
    print("=" * 60)
    print("[*] PHISHING URL DETECTION - MODEL TRAINING")
    print("[*] With Kaggle Dataset Integration (58,645+ URLs)")
    print("=" * 60)
    
    # ────────────────────────────────────────────
    #  STEP 1: Load ALL Data
    # ────────────────────────────────────────────
    print("\n" + "-" * 40)
    print("[Step 1] Loading datasets...")
    print("-" * 40)
    
    # Load Kaggle dataset (58,645 URLs)
    X_kaggle, y_kaggle = load_kaggle_dataset()
    
    # Load our sample URLs (100 URLs)
    X_sample, y_sample = load_sample_urls()
    
    # Combine both datasets
    if X_kaggle is not None:
        X = np.vstack([X_kaggle, X_sample])
        y = np.concatenate([y_kaggle, y_sample])
        print(f"\n  [+] COMBINED DATASET:")
        print(f"      Kaggle data:  {len(X_kaggle)} URLs")
        print(f"      Sample data:  {len(X_sample)} URLs")
        print(f"      TOTAL:        {len(X)} URLs")
    else:
        X = X_sample
        y = y_sample
        print(f"\n  [+] Using sample data only: {len(X)} URLs")
    
    print(f"  [+] Total Safe URLs:     {sum(y == 0)}")
    print(f"  [+] Total Phishing URLs: {sum(y == 1)}")
    print(f"  [+] Features per URL:    {X.shape[1]}")
    
    # ────────────────────────────────────────────
    #  STEP 2: Train/Test Split
    # ────────────────────────────────────────────
    print("\n" + "-" * 40)
    print("[Step 2] Splitting data into train/test...")
    print("-" * 40)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2,       # 20% test ke liye
        random_state=42,     # Reproducible results
        stratify=y           # Balanced classes
    )
    
    print(f"  [+] Training data: {len(X_train)} URLs")
    print(f"  [+] Testing data:  {len(X_test)} URLs")
    
    # ────────────────────────────────────────────
    #  STEP 3: Train Random Forest Model
    # ────────────────────────────────────────────
    print("\n" + "-" * 40)
    print("[Step 3] Training Random Forest model...")
    print("-" * 40)
    
    model = RandomForestClassifier(
        n_estimators=200,    # 200 decision trees (more trees = better)
        max_depth=15,        # Deeper trees for complex patterns
        min_samples_split=5, # Minimum samples to split a node
        min_samples_leaf=2,  # Minimum samples in a leaf
        random_state=42,     # Reproducible
        n_jobs=-1            # Use all CPU cores
    )
    
    print("  [*] Training with 200 trees, max_depth=15...")
    model.fit(X_train, y_train)
    print("  [+] Model training complete!")
    
    # ────────────────────────────────────────────
    #  STEP 4: Evaluate Model
    # ────────────────────────────────────────────
    print("\n" + "-" * 40)
    print("[Step 4] Evaluating model accuracy...")
    print("-" * 40)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n  *** MODEL ACCURACY: {accuracy * 100:.2f}% ***")
    
    print(f"\n  Classification Report:")
    print(classification_report(
        y_test, y_pred, 
        target_names=['Safe', 'Phishing']
    ))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("  Confusion Matrix:")
    print(f"                  Predicted Safe  Predicted Phishing")
    print(f"  Actual Safe       {cm[0][0]:>8}       {cm[0][1]:>8}")
    print(f"  Actual Phishing   {cm[1][0]:>8}       {cm[1][1]:>8}")
    
    # ────────────────────────────────────────────
    #  STEP 5: Feature Importance
    # ────────────────────────────────────────────
    print("\n" + "-" * 40)
    print("[Step 5] Feature importance ranking...")
    print("-" * 40)
    
    feature_names = get_feature_names()
    importances = model.feature_importances_
    
    indices = np.argsort(importances)[::-1]
    
    print("\n  Rank  Feature                    Importance")
    print("  " + "-" * 50)
    for i, idx in enumerate(indices):
        bar = "#" * int(importances[idx] * 50)
        print(f"  {i+1:2d}.   {feature_names[idx]:25s}  {importances[idx]:.4f}  {bar}")
    
    # ────────────────────────────────────────────
    #  STEP 6: Save Model
    # ────────────────────────────────────────────
    print("\n" + "-" * 40)
    print("[Step 6] Saving trained model...")
    print("-" * 40)
    
    model_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(model_dir, 'phishing_model.pkl')
    
    joblib.dump(model, model_path)
    print(f"  [+] Model saved: {model_path}")
    
    # Model info save karo
    model_info = {
        "accuracy": float(accuracy),
        "total_samples": int(len(X)),
        "kaggle_samples": int(len(X_kaggle)) if X_kaggle is not None else 0,
        "sample_urls": int(len(X_sample)),
        "safe_samples": int(sum(y == 0)),
        "phishing_samples": int(sum(y == 1)),
        "n_features": int(X.shape[1]),
        "n_estimators": 200,
        "max_depth": 15,
        "dataset_source": "Kaggle - GregaVrbancic/Phishing-Dataset (58,645 URLs) + Custom samples (100 URLs)",
        "feature_names": feature_names,
        "feature_importances": {
            feature_names[i]: float(importances[i]) 
            for i in range(len(feature_names))
        },
        "confusion_matrix": {
            "true_safe": int(cm[0][0]),
            "false_phishing": int(cm[0][1]),
            "false_safe": int(cm[1][0]),
            "true_phishing": int(cm[1][1])
        }
    }
    
    info_path = os.path.join(model_dir, 'model_info.json')
    with open(info_path, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"  [+] Model info saved: {info_path}")
    
    # ────────────────────────────────────────────
    #  STEP 7: Quick Test
    # ────────────────────────────────────────────
    print("\n" + "-" * 40)
    print("[Step 7] Quick test with sample URLs...")
    print("-" * 40)
    
    test_urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.flipkart.com",
        "http://192.168.1.1/login/secure/bank",
        "http://g00gle-secure-login.tk/verify",
        "http://bit.ly/3xFakeLink",
        "http://facebook.com@evil.com/login",
        "http://paytm-secure-login.tk/wallet/verify",
    ]
    
    print(f"\n  {'URL':<50} {'Result':<15} {'Confidence':<10}")
    print("  " + "-" * 75)
    
    for url in test_urls:
        features = np.array([extract_features(url)])
        pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0]
        confidence = max(prob) * 100
        
        result = "[X] PHISHING" if pred == 1 else "[OK] SAFE"
        print(f"  {url:<50} {result:<15} {confidence:.1f}%")
    
    # ────────────────────────────────────────────
    #  DONE!
    # ────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("[*] MODEL TRAINING COMPLETE!")
    print(f"[*] Dataset: {len(X)} URLs (Kaggle + Custom)")
    print(f"[*] Accuracy: {accuracy * 100:.2f}%")
    print("=" * 60)
    
    return model


if __name__ == "__main__":
    train_model()
