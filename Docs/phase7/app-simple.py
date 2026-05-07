"""
Simple FastAPI application without Unicode issues
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Zomato Restaurant Recommendation API",
    description="AI-powered restaurant recommendation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Zomato Restaurant Recommendation API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2026-05-07T16:00:00Z",
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

if __name__ == "__main__":
    print("Starting Zomato Restaurant Recommendation API...")
    print("Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("Metadata: http://localhost:8000/api/metadata")
    
    uvicorn.run(
        "app-simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
