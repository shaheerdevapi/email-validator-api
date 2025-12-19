from fastapi import FastAPI, Query
import uvicorn
import re

app = FastAPI()

DISPOSABLE_DOMAINS = {
    "tempmail.com", "mailinator.com", "yopmail.com"
}

@app.get("/")
def home():
    return {"API": "Email Validator", "status": "active"}

@app.get("/verify")
def verify(email: str = Query(...)):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    valid = bool(re.match(pattern, email))
    
    if not valid:
        return {"email": email, "valid": False}
    
    domain = email.split('@')[1].lower()
    disposable = domain in DISPOSABLE_DOMAINS
    
    return {
        "email": email,
        "valid": True,
        "disposable": disposable,
        "domain": domain
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
