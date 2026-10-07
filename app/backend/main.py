from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {
        "application": "Aspecta Backend",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/api/info")
def info():
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "message": os.getenv("APP_MESSAGE", "Hello from Aspecta Backend")
    }
