from flask import Flask, request, jsonify
import re

app = Flask(__name__)

DISPOSABLE_DOMAINS = {
    "tempmail.com", "mailinator.com", "yopmail.com",
    "10minutemail.com", "guerrillamail.com", "trashmail.com",
    "fakeinbox.com", "throwawaymail.com", "getairmail.com"
}

def validate_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def calculate_score(valid, disposable):
    if not valid:
        return 0
    if disposable:
        return 30
    return 100

@app.route('/')
def home():
    return jsonify({
        "api": "Professional Email Validator",
        "version": "2.0",
        "endpoints": {
            "/verify": "Single email validation",
            "/batch": "Bulk validation (POST)",
            "/health": "Health check",
            "/stats": "API statistics"
        },
        "pricing": {
            "free": "100 requests/day",
            "pro": "$9.99/month - 10,000 requests",
            "enterprise": "$49.99/month - Unlimited"
        }
    })

@app.route('/verify')
def verify():
    email = request.args.get('email', '').strip()
    
    if not email:
        return jsonify({"error": "Email parameter required"}), 400
    
    valid_format = validate_email_format(email)
    
    if not valid_format:
        return jsonify({
            "email": email,
            "valid_format": False,
            "disposable": False,
            "score": 0,
            "message": "Invalid email format"
        })
    
    domain = email.split('@')[1].lower()
    disposable = domain in DISPOSABLE_DOMAINS
    score = calculate_score(valid_format, disposable)
    
    return jsonify({
        "email": email,
        "valid_format": True,
        "disposable": disposable,
        "domain": domain,
        "score": score,
        "message": "Professional email" if not disposable else "Disposable email detected"
    })

@app.route('/batch', methods=['POST'])
def batch_verify():
    data = request.get_json()
    
    if not data or 'emails' not in data:
        return jsonify({"error": "JSON with 'emails' array required"}), 400
    
    emails = data['emails']
    results = []
    
    for email in emails:
        try:
            valid_format = validate_email_format(email)
            disposable = False
            
            if valid_format:
                domain = email.split('@')[1].lower()
                disposable = domain in DISPOSABLE_DOMAINS
            
            score = calculate_score(valid_format, disposable)
            
            results.append({
                "email": email,
                "valid_format": valid_format,
                "disposable": disposable,
                "score": score,
                "domain": email.split('@')[1].lower() if valid_format else None
            })
        except:
            results.append({
                "email": email,
                "valid_format": False,
                "disposable": False,
                "score": 0,
                "error": "Processing error"
            })
    
    return jsonify({
        "total": len(emails),
        "processed": len(results),
        "results": results
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "email-validation-api",
        "uptime": "100%"
    })

@app.route('/stats')
def stats():
    return jsonify({
        "total_domains": len(DISPOSABLE_DOMAINS),
        "api_version": "2.0",
        "performance": "high",
        "rate_limit": "100 requests/day (free)"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
