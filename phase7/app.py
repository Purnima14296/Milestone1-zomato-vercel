"""
Phase 7 FastAPI Application: Main web server application.

This module creates and configures the FastAPI application with all
API endpoints, middleware, and error handling for the restaurant
recommendation system.
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime
from typing import Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from models import ErrorResponse
from health_api import HealthAPI
from recommendation_api import RecommendationAPI
from metadata_api import MetadataAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("🚀 Starting Zomato Recommendation API...")
    start_time = time.time()
    
    # Initialize components
    app.state.start_time = start_time
    app.state.request_count = 0
    app.state.error_count = 0
    
    print(f"✅ API started in {time.time() - start_time:.2f} seconds")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Zomato Recommendation API...")


def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    
    # Create FastAPI app
    app = FastAPI(
        title="Zomato Restaurant Recommendation API",
        description="AI-powered restaurant recommendation system with comprehensive evaluation and monitoring",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # Add middleware
    setup_middleware(app)
    
    # Add exception handlers
    setup_exception_handlers(app)
    
    # Add API routes
    setup_routes(app)
    
    # Add custom OpenAPI
    setup_openapi(app)
    
    return app


def setup_middleware(app: FastAPI) -> None:
    """Setup application middleware."""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # GZip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        print(f"[{request_id}] {request.method} {request.url}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        # Update counters
        app.state.request_count += 1
        
        # Log response
        print(f"[{request_id}] {response.status_code} - {process_time:.3f}s")
        
        return response


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup custom exception handlers."""
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Handle HTTP exceptions."""
        app.state.error_count += 1
        
        error_response = ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.detail,
            details={"status_code": exc.status_code},
            timestamp=datetime.utcnow(),
            request_id=getattr(request.state, "request_id", None)
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.dict()
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        """Handle value errors."""
        app.state.error_count += 1
        
        error_response = ErrorResponse(
            error="ValidationError",
            message=str(exc),
            timestamp=datetime.utcnow(),
            request_id=getattr(request.state, "request_id", None)
        )
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.dict()
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle general exceptions."""
        app.state.error_count += 1
        
        error_response = ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
            details={"exception_type": exc.__class__.__name__},
            timestamp=datetime.utcnow(),
            request_id=getattr(request.state, "request_id", None)
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.dict()
        )


def setup_routes(app: FastAPI) -> None:
    """Setup API routes."""
    
    # Initialize API components
    health_api = HealthAPI()
    recommendation_api = RecommendationAPI()
    metadata_api = MetadataAPI()
    
    # Include routers
    app.include_router(health_api.router)
    app.include_router(recommendation_api.router)
    app.include_router(metadata_api.router)
    
    # Add root endpoint
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "Zomato Restaurant Recommendation API",
            "version": "1.0.0",
            "description": "AI-powered restaurant recommendation system",
            "docs_url": "/docs",
            "health_url": "/api/health",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": time.time() - app.state.start_time
        }
    
    # Add restaurant search endpoint
    @app.get("/api/restaurants/search", tags=["restaurants"])
    async def search_restaurants(
        location: str = None,
        cuisine: str = None,
        min_rating: float = None,
        max_cost: float = None,
        limit: int = 20,
        offset: int = 0
    ):
        """Search restaurants with filters."""
        try:
            # For demo purposes, return sample data
            # In production, this would query the database
            sample_restaurants = [
                {
                    "name": "Byg Brewski Brewing Company",
                    "city": location or "Bellandur",
                    "cuisines": ["Continental", "North Indian", "Italian"],
                    "rating": 4.9,
                    "cost_estimate": 1600,
                    "reason": "Popular brewery with excellent ambiance"
                },
                {
                    "name": "The Black Pearl",
                    "city": location or "Bellandur",
                    "cuisines": ["North Indian", "European", "Mediterranean"],
                    "rating": 4.8,
                    "cost_estimate": 1500,
                    "reason": "Fine dining experience with great service"
                }
            ]
            
            # Apply filters (simplified)
            filtered_restaurants = sample_restaurants
            
            if min_rating:
                filtered_restaurants = [r for r in filtered_restaurants if r["rating"] >= min_rating]
            
            if max_cost:
                filtered_restaurants = [r for r in filtered_restaurants if r["cost_estimate"] <= max_cost]
            
            # Apply pagination
            paginated_restaurants = filtered_restaurants[offset:offset + limit]
            
            return {
                "restaurants": paginated_restaurants,
                "total": len(filtered_restaurants),
                "limit": limit,
                "offset": offset
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Restaurant search failed: {str(e)}"
            )
    
    # Add preference validation endpoint
    @app.post("/api/preferences/validate", tags=["preferences"])
    async def validate_preferences(preferences: dict):
        """Validate user preferences."""
        try:
            errors = []
            warnings = []
            suggestions = []
            
            # Validate location
            if not preferences.get("location"):
                errors.append({
                    "field": "location",
                    "message": "Location is required",
                    "severity": "error"
                })
            
            # Validate budget
            budget = preferences.get("budget", {})
            if not isinstance(budget, dict):
                errors.append({
                    "field": "budget",
                    "message": "Budget must be an object with min and max values",
                    "severity": "error"
                })
            else:
                if budget.get("min", 0) < 0:
                    errors.append({
                        "field": "budget.min",
                        "message": "Minimum budget cannot be negative",
                        "severity": "error"
                    })
                
                if budget.get("max", 0) <= budget.get("min", 0):
                    errors.append({
                        "field": "budget.max",
                        "message": "Maximum budget must be greater than minimum budget",
                        "severity": "error"
                    })
            
            # Validate rating
            min_rating = preferences.get("minimum_rating", 0)
            if min_rating < 0 or min_rating > 5:
                errors.append({
                    "field": "minimum_rating",
                    "message": "Minimum rating must be between 0 and 5",
                    "severity": "error"
                })
            
            # Add suggestions
            if preferences.get("minimum_rating", 0) > 4.5:
                suggestions.append("Consider lowering the minimum rating to get more options")
            
            if budget.get("max", 0) < 500:
                suggestions.append("Consider increasing the budget for better restaurant options")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings,
                "suggestions": suggestions
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Preference validation failed: {str(e)}"
            )


def setup_openapi(app: FastAPI) -> None:
    """Setup custom OpenAPI schema."""
    
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title="Zomato Restaurant Recommendation API",
            version="1.0.0",
            description="""
            ## AI-Powered Restaurant Recommendation System
            
            This API provides intelligent restaurant recommendations using advanced
            machine learning algorithms and natural language processing.
            
            ### Key Features:
            - 🤖 AI-powered recommendations
            - 🍽️ Multi-cuisine support
            - 💰 Budget-based filtering
            - ⭐ Rating-based sorting
            - 📍 Location-specific results
            - 📊 Real-time metrics
            - 🔍 Restaurant search
            - ✅ Preference validation
            
            ### Getting Started:
            1. Check system health: `GET /api/health`
            2. Get system metadata: `GET /api/metadata`
            3. Generate recommendations: `POST /api/recommendations`
            4. Search restaurants: `GET /api/restaurants/search`
            """,
            routes=app.routes,
        )
        
        # Add custom schemas
        openapi_schema["components"]["schemas"] = {
            **openapi_schema.get("components", {}).get("schemas", {}),
        }
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi


# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    print("Starting Zomato Restaurant Recommendation API...")
    print("Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("Metadata: http://localhost:8000/api/metadata")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
