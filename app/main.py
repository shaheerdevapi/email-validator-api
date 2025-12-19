from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import re
from typing import Dict, List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DISPOSABLE_DOMAINS = {
    "tempmail.com", "mailinator.com", "yopmail.com",
    "10minutemail.com", "guerrillamail.com", "trashmail.com",
    "fakeinbox.com", "throwawaymail.com", "getairmail.com",
    "sharklasers.com", "guerrillamail.info", "dispostable.com"
}

def validate_email_format(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_disposable_domain(domain: str) -> bool:
    return domain.lower() in DISPOSABLE_DOMAINS

def get_email_score(email: str, valid: bool, disposable: bool) -> int:
    if not valid:
        return 0
    if disposable:
        return 30
    return 100

@app.get("/")
def root() -> Dict:
    return {
        "api": "Email Verification API",
        "version": "2.0.0",
        "status": "active",
        "endpoints": {
            "/verify": "GET - Verify single email",
            "/batch": "POST - Verify multiple emails",
            "/health": "GET - Health check",
            "/stats": "GET - API statistics"
        }
    }

@app.get("/verify")
def verify_email(email: str = Query(...)):
    if not email:
        raise HTTPException(status_code=400, detail="Email parameter required")
    
    valid_format = validate_email_format(email)
    
    if not valid_format:
        return {
            "email": email,
            "valid_format": False,
            "disposable": False,
            "score": 0,
            "error": "Invalid email format"
        }
    
    domain = email.split('@')[1].lower()
    is_disposable = is_disposable_domain(domain)
    score = get_email_score(email, valid_format, is_disposable)
    
    return {
        "email": email,
        "valid_format": True,
        "disposable": is_disposable,
        "score": score,
        "domain": domain,
        "message": "Valid email" if not is_disposable else "Disposable email detected"
    }

@app.get("/health")
def health_check() -> Dict:
    return {"status": "healthy", "service": "email-verification-api"}

@app.get("/stats")
def get_stats() -> Dict:
    return {
        "total_disposable_domains": len(DISPOSABLE_DOMAINS),
        "api_version": "2.0.0",
        "features": ["format_check", "disposable_check", "scoring"],
        "rate_limit": "unlimited"
    }

@app.post("/batch")
def batch_verify(emails: List[str]) -> Dict:
    if not emails:
        raise HTTPException(status_code=400, detail="Email list cannot be empty")
    
    results = []
    for email in emails:
        try:
            valid_format = validate_email_format(email)
            disposable = False
            domain = None
            
            if valid_format:
                domain = email.split('@')[1].lower()
                disposable = is_disposable_domain(domain)
            
            score = get_email_score(email, valid_format, disposable)
            
            results.append({
                "email": email,
                "valid_format": valid_format,
                "disposable": disposable,
                "score": score,
                "domain": domain if domain else None
            })
        except Exception:
            results.append({
                "email": email,
                "valid_format": False,
                "disposable": False,
                "score": 0,
                "error": "Processing error"
            })
    
    return {
        "total_emails": len(emails),
        "processed": len(results),
        "results": results
    }

@app.get("/domains/list")
def list_disposable_domains() -> Dict:
    return {
        "count": len(DISPOSABLE_DOMAINS),
        "domains": sorted(list(DISPOSABLE_DOMAINS))
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
