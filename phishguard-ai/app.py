from flask import Flask, render_template, request, jsonify
from phishing_detector import analyze_url, analyze_email
from api_checker import check_url_reputation

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the main homepage of the application.
    """
    return render_template('index.html')

@app.route('/scan_url', methods=['POST'])
def scan_url():
    """
    API endpoint to scan a URL.
    Receives JSON data containing the URL and returns the analysis and reputation results.
    """
    # Get JSON data from the frontend request
    data = request.get_json()
    url = data.get('url', '')
    
    # Check if a URL was actually provided
    if not url:
        return jsonify({"error": "No URL provided"}), 400
        
    # 1. Run our rule-based phishing detection
    analysis_result = analyze_url(url)
    
    # 2. Simulate checking the URL against a reputation API (e.g., VirusTotal)
    api_result = check_url_reputation(url)
    
    # Combine both results and send back to the frontend
    return jsonify({
        "analysis": analysis_result,
        "api_reputation": api_result
    })

@app.route('/scan_email', methods=['POST'])
def scan_email():
    """
    API endpoint to scan email text.
    Receives JSON data containing the email text and returns the analysis results.
    """
    # Get JSON data from the frontend request
    data = request.get_json()
    email_text = data.get('text', '')
    
    # Check if text was provided
    if not email_text:
        return jsonify({"error": "No email text provided"}), 400
        
    # Run our rule-based phishing detection on the email text
    analysis_result = analyze_email(email_text)
    
    # Send the results back to the frontend
    return jsonify({
        "analysis": analysis_result
    })

# Run the Flask app
if __name__ == '__main__':
    # Running on debug mode for development purposes
    app.run(debug=True, port=5000)
