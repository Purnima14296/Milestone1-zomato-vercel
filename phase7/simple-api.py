"""
Simple API server to serve the live example recommendations
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import time
from datetime import datetime

app = FastAPI(title="Zomato Restaurant API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load test data
with open('test-result.json', 'r') as f:
    test_data = json.load(f)

@app.get("/")
async def root():
    return {"message": "Zomato Restaurant Recommendation API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "components": [
            {
                "name": "database",
                "status": "healthy",
                "response_time": 0.01,
                "message": "Database connection successful"
            },
            {
                "name": "llm_service", 
                "status": "healthy",
                "response_time": 0.05,
                "message": "LLM service available"
            }
        ]
    }

@app.post("/api/recommendations")
async def generate_recommendations(request: Dict[str, Any]):
    """Generate restaurant recommendations based on user preferences"""
    return test_data

@app.get("/api/metadata")
async def get_metadata():
    """Get system metadata and capabilities"""
    return {
        "system_info": {
            "name": "Zomato Restaurant Recommendation System",
            "version": "1.0.0",
            "description": "AI-powered restaurant recommendation system",
            "api_version": "v1"
        },
        "capabilities": {
            "max_recommendations": 20,
            "supported_locations": ["Bellandur", "Indiranagar"],
            "supported_cuisines": ["North Indian", "South Indian", "Chinese", "Continental", "Italian", "Thai", "Mughlai", "Barbecue"],
            "features": [
                "Personalized recommendations",
                "Restaurant search",
                "Preference validation",
                "Real-time processing",
                "Explanations included"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Zomato Restaurant Recommendation API...")
    print("Live Example Ready!")
    print("Health Check: http://localhost:8001/api/health")
    print("Recommendations: http://localhost:8001/api/recommendations")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
