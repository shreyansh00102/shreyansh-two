"""
=============================================================
  FEATURE EXTRACTOR — URL se Features Nikalne ka Code
=============================================================
  Ye file URL ko analyze karke usse features nikalti hai.
  Har feature ek number hai jo batata hai ki URL suspicious
  hai ya nahi.
  
  Example:
    URL: "http://192.168.1.1/login/secure/bank"
    Features: [35, 1, 3, 0, 0, 0, 3, 0, 3, 0, 5, 11, 4, 1, 0]
=============================================================
"""

import re
from urllib.parse import urlparse

# ---- URL Shortening services ki list ----
SHORTENING_SERVICES = [
    'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly',
    'is.gd', 'buff.ly', 'adf.ly', 'tiny.cc', 'lnkd.in',
    'shorte.st', 'cli.gs', 'x.co', 'yourls.org', 'v.gd',
    'tr.im', 'link.zip.net', 'rb.gy'
]

# ---- Suspicious words jo phishing URLs mein hote hain ----
SUSPICIOUS_WORDS = [
    'login', 'signin', 'verify', 'secure', 'account',
    'update', 'bank', 'confirm', 'password', 'credential',
    'suspend', 'restrict', 'alert', 'urgent', 'expire',
    'wallet', 'paypal', 'netflix', 'apple', 'microsoft'
]


def extract_features(url):
    """
    Ek URL se saari features nikalta hai.
    
    Input:  url (string) — e.g., "https://www.google.com"
    Output: list of numbers — e.g., [19, 0, 2, 0, ...]
    
    Har feature ka matlab neeche explain hai.
    """
    features = []
    
    # URL ko parse karo (parts mein todo)
    try:
        parsed = urlparse(url)
        domain = parsed.netloc    # e.g., "www.google.com"
        path = parsed.path        # e.g., "/search/results"
        scheme = parsed.scheme    # e.g., "https"
    except:
        # Agar URL parse nahi ho paaye toh default values
        parsed = None
        domain = ""
        path = ""
        scheme = ""
    
    url_lower = url.lower()
    
    # ===== FEATURE 1: URL Length =====
    # Phishing URLs zyada lambi hoti hain
    # Safe: < 54 chars | Suspicious: 54-75 | Phishing: > 75
    url_length = len(url)
    features.append(url_length)
    
    # ===== FEATURE 2: Has IP Address? =====
    # Agar domain mein IP address hai toh suspicious hai
    # Example: http://192.168.1.1/login → PHISHING
    has_ip = 1 if re.match(
        r'(\d{1,3}\.){3}\d{1,3}', domain
    ) else 0
    features.append(has_ip)
    
    # ===== FEATURE 3: Number of Dots =====
    # Zyada dots = zyada subdomains = suspicious
    # Example: "a.b.c.d.evil.com" → 5 dots = PHISHING
    num_dots = url.count('.')
    features.append(num_dots)
    
    # ===== FEATURE 4: Has @ Symbol? =====
    # @ symbol browser ko confuse karta hai
    # Example: http://google.com@evil.com → PHISHING
    has_at = 1 if '@' in url else 0
    features.append(has_at)
    
    # ===== FEATURE 5: Has Double Slash Redirect? =====
    # Path mein // hona redirect trick hai
    # Example: http://google.com//evil.com → PHISHING
    has_double_slash = 1 if '//' in path else 0
    features.append(has_double_slash)
    
    # ===== FEATURE 6: Has Dash in Domain? =====
    # Legitimate domains mein dash kam hota hai
    # Example: "google-login-secure.com" → SUSPICIOUS
    has_dash = 1 if '-' in domain else 0
    features.append(has_dash)
    
    # ===== FEATURE 7: Number of Subdomains =====
    # Zyada subdomains = suspicious
    # "www.google.com" → 1 subdomain (ok)
    # "a.b.c.google.com" → 3 subdomains (suspicious)
    num_subdomains = len(domain.split('.')) - 2 if domain else 0
    num_subdomains = max(0, num_subdomains)
    features.append(num_subdomains)
    
    # ===== FEATURE 8: Is HTTPS? =====
    # HTTPS = safer (but not always)
    # http:// → 0 (not secure) | https:// → 1 (secure)
    is_https = 1 if scheme == 'https' else 0
    features.append(is_https)
    
    # ===== FEATURE 9: URL Depth (Path Depth) =====
    # URL mein kitne "/" hain — deep paths suspicious hain
    # "/login" → depth 1 | "/a/b/c/d" → depth 4
    url_depth = len([p for p in path.split('/') if p])
    features.append(url_depth)
    
    # ===== FEATURE 10: Uses URL Shortener? =====
    # bit.ly, tinyurl.com etc. phishing mein use hote hain
    has_shortening = 1 if any(
        service in url_lower for service in SHORTENING_SERVICES
    ) else 0
    features.append(has_shortening)
    
    # ===== FEATURE 11: Number of Special Characters =====
    # Zyada special chars = suspicious
    # Characters: %, =, &, ?, #, ~, !
    special_chars = re.findall(r'[%=&?#~!]', url)
    num_special = len(special_chars)
    features.append(num_special)
    
    # ===== FEATURE 12: Domain Length =====
    # Bohot lamba domain name = suspicious
    # "google.com" → 10 (ok) | "g00gle-secure-login-page.com" → 28 (bad)
    domain_length = len(domain)
    features.append(domain_length)
    
    # ===== FEATURE 13: Number of Digits in Domain =====
    # Legitimate domains mein numbers kam hote hain
    # "g00gle.com" → 2 digits (suspicious)
    num_digits = len(re.findall(r'\d', domain))
    features.append(num_digits)
    
    # ===== FEATURE 14: Has Suspicious Words? =====
    # "login", "verify", "secure", "bank" etc.
    has_suspicious = 1 if any(
        word in url_lower for word in SUSPICIOUS_WORDS
    ) else 0
    features.append(has_suspicious)
    
    # ===== FEATURE 15: Has URL Encoding? =====
    # %20, %3D etc. = encoded characters = suspicious
    has_encoding = 1 if '%' in url else 0
    features.append(has_encoding)
    
    return features


def get_feature_names():
    """Feature names ki list return karta hai (for reference)."""
    return [
        'url_length',
        'has_ip_address',
        'num_dots',
        'has_at_symbol',
        'has_double_slash',
        'has_dash_in_domain',
        'num_subdomains',
        'is_https',
        'url_depth',
        'uses_shortener',
        'num_special_chars',
        'domain_length',
        'num_digits_in_domain',
        'has_suspicious_words',
        'has_url_encoding'
    ]


def get_reasons(url):
    """
    URL ke suspicious points ki list banata hai.
    Ye user ko dikhaya jaayega ki URL kyun phishing hai, with bilingual details.
    """
    reasons = []
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        scheme = parsed.scheme
    except:
        domain = ""
        path = ""
        scheme = ""
    
    url_lower = url.lower()
    
    # 1. URL Length Check
    if len(url) > 75:
        reasons.append({
            "icon": "📏",
            "title_en": "URL is extremely long",
            "title_hi": "URL Bahut Lambi Hai",
            "detail_en": f"URL contains {len(url)} characters. Phishers use long URLs to hide the actual malicious domain and mimic trusted links.",
            "detail_hi": f"URL mein {len(url)} letters hain. Phishers lambi URLs ka use karte hain taaki asli domain name chhup sake aur link trusted lage.",
            "severity": "high",
            "highlight_type": "length",
            "highlight_target": url
        })
    elif len(url) > 54:
        reasons.append({
            "icon": "📏",
            "title_en": "URL is slightly long",
            "title_hi": "URL Thodi Lambi Hai",
            "detail_en": f"URL contains {len(url)} characters. Moderately long links often contain confusing words to misdirect users.",
            "detail_hi": f"URL mein {len(url)} letters hain. Thodi lambi URLs mein extra words add kiye jaate hain taaki user confuse ho sake.",
            "severity": "medium",
            "highlight_type": "length",
            "highlight_target": url
        })
    
    # 2. IP Address Check
    ip_match = re.search(r'(\d{1,3}\.){3}\d{1,3}', domain)
    if ip_match:
        reasons.append({
            "icon": "🔢",
            "title_en": "IP Address in Domain",
            "title_hi": "Domain Mein IP Address Hai",
            "detail_en": "Legitimate websites always use brand names (e.g., google.com), not raw numbers. This is a 99% indicator of a malicious scam.",
            "detail_hi": "Asli websites hamesha brand name use karti hain, raw numbers (IP) nahi. IP address use karna lagbhag pakka scam ka sanket hai.",
            "severity": "critical",
            "highlight_type": "ip",
            "highlight_target": ip_match.group(0)
        })
    
    # 3. @ Symbol Check
    if '@' in url:
        reasons.append({
            "icon": "📧",
            "title_en": "@ Symbol Detected",
            "title_hi": "URL Mein @ Symbol Mila",
            "detail_en": "The '@' symbol makes the browser ignore everything before it, silently redirecting you to a malicious destination afterwards.",
            "detail_hi": "URL mein '@' symbol browser ko iske pehle ka sab ignore karne par majboor karta hai aur aapko dangerous destination page par bhejta hai.",
            "severity": "critical",
            "highlight_type": "at",
            "highlight_target": "@"
        })
    
    # 4. Double Slash Redirect Check
    if '//' in path:
        reasons.append({
            "icon": "↗️",
            "title_en": "Double Slash Redirect Trick",
            "title_hi": "Double Slash (//) Redirect Mila",
            "detail_en": "Using '//' inside the path is an old redirection trick used by phishers to mask the destination page.",
            "detail_hi": "URL path ke andar '//' use karna ek stealthy redirect trick hai jo aapko dhokhe se dusri site par bhejti hai.",
            "severity": "high",
            "highlight_type": "double_slash",
            "highlight_target": "//"
        })
    
    # 5. Dash in Domain Check
    if '-' in domain:
        reasons.append({
            "icon": "➖",
            "title_en": "Dash (-) in Domain Name",
            "title_hi": "Domain Name Mein Dash (-) Hai",
            "detail_en": "Legitimate brands rarely use dashes in their domains. Attackers use it to spoof real names (e.g., facebook-secure.com).",
            "detail_hi": "Asli brands domain mein dash (-) kam use karte hain. Phishers iska use fake names banane ke liye karte hain (jaise netflix-secure.com).",
            "severity": "medium",
            "highlight_type": "dash",
            "highlight_target": "-"
        })
    
    # 6. Too Many Dots / Subdomains Check
    dot_count = domain.count('.')
    if dot_count > 3:
        reasons.append({
            "icon": "🔵",
            "title_en": "Excessive Subdomains",
            "title_hi": "Bahut Saare Subdomains Hain",
            "detail_en": f"Found {dot_count} dots in domain. Too many subdomains are used to spoof trusted brand names (e.g., paypal.com.login-verify.xyz).",
            "detail_hi": f"Domain mein {dot_count} dots hain. Bahut saare subdomains ka use brand name copy karne ke liye kiya jata hai (jaise paypal.com.login.evil.com).",
            "severity": "high",
            "highlight_type": "dots",
            "highlight_target": domain
        })
    
    # 7. HTTPS Check
    if scheme != 'https':
        reasons.append({
            "icon": "🔓",
            "title_en": "Insecure Connection (No HTTPS)",
            "title_hi": "Insecure Connection (HTTPS Missing)",
            "detail_en": "The website does not use SSL/TLS encryption. Any passwords, credit cards, or logins you enter can be intercepted by hackers.",
            "detail_hi": "Site secure connection (HTTPS) use nahi kar rahi hai. Yahan enter kiya gaya koi bhi password ya details chori ho sakti hain.",
            "severity": "medium",
            "highlight_type": "http",
            "highlight_target": "http://"
        })
    
    # 8. URL Shortener Check
    shortener_found = [s for s in SHORTENING_SERVICES if s in url_lower]
    if shortener_found:
        reasons.append({
            "icon": "🔗",
            "title_en": "URL Shortener Detected",
            "title_hi": "URL Shortener Ka Use Hua Hai",
            "detail_en": f"Short links (using {shortener_found[0]}) hide the actual destination URL, which is a classic way to mask a phishing trap.",
            "detail_hi": f"Short links ({shortener_found[0]} ka use karke) asli link ko chupati hain, jo malicious site ko chupaane ke liye use hota hai.",
            "severity": "high",
            "highlight_type": "shortener",
            "highlight_target": shortener_found[0]
        })
    
    # 9. Suspicious Words Check
    suspicious_found = [w for w in SUSPICIOUS_WORDS if w in url_lower]
    if suspicious_found:
        reasons.append({
            "icon": "⚠️",
            "title_en": "Suspicious Brand/Action Words",
            "title_hi": "Shakki Words Mile",
            "detail_en": f"Words like '{', '.join(suspicious_found)}' in unofficial domains are intended to deceive you into typing credentials.",
            "detail_hi": f"Domain mein '{', '.join(suspicious_found)}' jaise words ka use aapka password/credit card details churane ke liye hota hai.",
            "severity": "high",
            "highlight_type": "suspicious_words",
            "highlight_target": suspicious_found[0]
        })
    
    # 10. URL Encoding Check
    if '%' in url:
        reasons.append({
            "icon": "🔡",
            "title_en": "Obfuscated URL Encoding",
            "title_hi": "URL Encoding (Chhupe Akshar)",
            "detail_en": "Encoded characters (like %20, %3D) are used to bypass browser security filters and hide malicious text from users.",
            "detail_hi": "%20 ya %3D jaise encoded letters ka use malicious links ko chupati hain taaki security filters ise pakad na sakein.",
            "severity": "medium",
            "highlight_type": "encoding",
            "highlight_target": "%"
        })
    
    # 11. Excess Digits in Domain Check
    digits_in_domain = len(re.findall(r'\d', domain))
    if digits_in_domain > 3:
        reasons.append({
            "icon": "🔢",
            "title_en": "Excessive Digits in Domain",
            "title_hi": "Domain Name Mein Bahut Numbers Hain",
            "detail_en": f"Found {digits_in_domain} digits in the domain name. Phishers add random numbers to recreate cloned versions of real brands.",
            "detail_hi": f"Domain name mein {digits_in_domain} numbers hain. Phishers numbers add karke lookalike websites banate hain (jaise paypa1.com).",
            "severity": "medium",
            "highlight_type": "digits",
            "highlight_target": domain
        })
    
    # Clean fallback reasons
    if not reasons:
        reasons.append({
            "icon": "✅",
            "title_en": "No Suspicious Features Detected",
            "title_hi": "Koi Suspicious Feature Nahi Mili",
            "detail_en": "This URL passes all standard heuristic tests. The structure appears legitimate.",
            "detail_hi": "Yeh URL sabhi standard criteria par sahi utra hai. Iska structure normal aur safe dikh raha hai.",
            "severity": "safe",
            "highlight_type": "none",
            "highlight_target": ""
        })
    
    return reasons


# ---- Test (agar direct run karo toh) ----
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/login/secure/bank",
        "https://g00gle-secure-login.tk/verify?user=admin",
        "http://bit.ly/3xAbCdE",
    ]
    
    print("=" * 60)
    print("FEATURE EXTRACTOR TEST")
    print("=" * 60)
    
    for url in test_urls:
        features = extract_features(url)
        reasons = get_reasons(url)
        print(f"\nURL: {url}")
        print(f"Features: {features}")
        print(f"Reasons: {len(reasons)} suspicious points found")
        for r in reasons:
            print(f"  {r['icon']} {r['title']}: {r['detail']}")
        print("-" * 40)
