def analyze_url(url):
    """
    Analyzes a URL for common phishing patterns and calculates a risk score.
    Returns a dictionary containing the final score, the reasons, and a risk level.
    """
    score = 0
    reasons = []

    # --- 1. Check for very long URLs ---
    # Phishing links are often excessively long to hide the actual domain
    if len(url) > 75:
        score += 1
        reasons.append("URL is unusually long (+1)")

    # --- 2. Check for suspicious symbols ---
    # The '@' symbol can be used to bypass the domain parsing in browsers
    if "@" in url:
        score += 1
        reasons.append("URL contains '@' symbol, often used to hide the real domain (+1)")
    
    # Phishers often use multiple hyphens to look like a legitimate domain (e.g. www.paypal-update-account.com)
    if url.count("-") > 3:
        score += 1
        reasons.append("URL contains multiple hyphens (+1)")
        
    # Subdomains can act like folders (e.g. secure.login.bank.com)
    if url.count(".") > 3:
        score += 1
        reasons.append("URL contains multiple subdomains/dots (+1)")

    # --- 3. Check for suspicious keywords ---
    # These keywords are heavily used in social engineering attacks
    suspicious_keywords = ["login", "verify", "bank", "secure", "update", "account"]
    
    # Convert url to lowercase for case-insensitive matching
    url_lower = url.lower()
    for keyword in suspicious_keywords:
        if keyword in url_lower:
            score += 2
            reasons.append(f"Suspicious keyword found: '{keyword}' (+2)")

    # --- 4. Determine final risk level based on the score ---
    if score >= 3:
        level = "DANGEROUS"
    elif score >= 1:
        level = "SUSPICIOUS"
    else:
        level = "SAFE"

    # Return the findings
    return {
        "score": score,
        "reasons": reasons,
        "level": level
    }


def analyze_email(text):
    """
    Analyzes email body text for phishing keywords and calculates a risk score.
    Returns a dictionary containing the final score, the reasons, and a risk level.
    """
    score = 0
    reasons = []
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # --- Check for common phishing phrases ---
    phishing_phrases = {
        "urgent": 2,
        "click here": 2,
        "verify account": 2,
        "password reset": 2,
        "account suspended": 2,
        "limited time": 1,
        "immediate action": 1,
        "kindly": 1
    }
    
    for phrase, points in phishing_phrases.items():
        if phrase in text_lower:
            score += points
            reasons.append(f"Suspicious phrase found: '{phrase}' (+{points})")
            
    # --- Determine final risk level based on the score ---
    # Note: Thresholds can be adjusted based on desired strictness
    if score >= 4:
        level = "DANGEROUS"
    elif score >= 2:
        level = "SUSPICIOUS"
    else:
        level = "SAFE"

    # Return the findings
    return {
        "score": score,
        "reasons": reasons,
        "level": level
    }
