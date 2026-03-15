import time
import random

def check_url_reputation(url):
    """
    Simulates checking a URL against a reputation API (like VirusTotal or Google Safe Browsing).
    
    In a real-world scenario, you would use the 'requests' library to make an HTTP call
    to the API provider, passing your API key and the URL to be checked.
    """
    
    # Simulate the network delay of calling an external API (1 second)
    time.sleep(1)
    
    # For demonstration purposes, we will simulate the result.
    # We will hardcode some universally known safe domains.
    known_safe_domains = ["google.com", "github.com", "wikipedia.org", "python.org", "microsoft.com"]
    
    # Check if the URL contains any of our known safe domains
    is_known_safe = any(domain in url.lower() for domain in known_safe_domains)
    
    if is_known_safe:
        return {
            "api_status": "Clean",
            "api_details": "No security vendors flagged this URL as malicious."
        }
    
    # To make our simulation interesting, we will randomly flag some unknown URLs.
    # Or definitely flag URLs that look obviously fake for our simulation.
    if "update" in url.lower() or "verify" in url.lower() or random.random() < 0.2:
        return {
            "api_status": "Malicious",
            "api_details": "2 security vendors flagged this URL as phishing/malicious."
        }
        
    # If the URL is custom but not explicitly flagged in our random logic
    return {
        "api_status": "Clean (Unrated)",
        "api_details": "No security vendors have flagged this URL, but proceed with caution."
    }
