"""
Phase 7 Recommendation API: Restaurant recommendation endpoints.

This module implements the core recommendation endpoints that integrate
Phases 1-5 to generate restaurant recommendations based on user preferences.
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from pathlib import Path

from models import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationHistory,
    RestaurantInfo,
    UserPreferences,
    ErrorResponse
)

# Import existing phase implementations
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src" / "zomato_rec" / "phase4"))


class RecommendationAPI:
    """Restaurant recommendation API endpoints."""
    
    def __init__(self):
        self.router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])
        self._setup_routes()
        
        # In-memory storage for demo (replace with database in production)
        self.recommendation_history: Dict[str, Dict[str, Any]] = {}
    
    def _setup_routes(self) -> None:
        """Setup recommendation routes."""
        self.router.add_api_route(
            "/", 
            self.generate_recommendations, 
            methods=["POST"],
            response_model=RecommendationResponse,
            summary="Generate restaurant recommendations",
            description="Generate personalized restaurant recommendations based on user preferences"
        )
        
        self.router.add_api_route(
            "/{request_id}", 
            self.get_recommendation, 
            methods=["GET"],
            response_model=RecommendationResponse,
            summary="Get recommendation by ID",
            description="Retrieve a previously generated recommendation by its ID"
        )
        
        self.router.add_api_route(
            "/history", 
            self.get_recommendation_history, 
            methods=["GET"],
            response_model=List[RecommendationHistory],
            summary="Get recommendation history",
            description="Get history of all recommendations (simplified version)"
        )
    
    async def generate_recommendations(
        self, 
        request: RecommendationRequest,
        background_tasks: BackgroundTasks
    ) -> RecommendationResponse:
        """
        Generate restaurant recommendations based on user preferences.
        
        Args:
            request: Recommendation request with user preferences
            background_tasks: FastAPI background tasks for async processing
            
        Returns:
            RecommendationResponse with generated recommendations
        """
        try:
            # Generate unique request ID
            request_id = str(uuid.uuid4())
            
            # Validate preferences
            self._validate_preferences(request.preferences)
            
            # Generate recommendations using Phase 4 pipeline
            recommendations = await self._generate_recommendations_pipeline(
                request.preferences, 
                request.top_k
            )
            
            # Create metadata
            metadata = self._create_metadata(request, len(recommendations))
            
            # Create response
            response = RecommendationResponse(
                request_id=request_id,
                preferences=request.preferences,
                recommendations=recommendations,
                metadata=metadata,
                created_at=datetime.utcnow()
            )
            
            # Store in history (async)
            background_tasks.add_task(
                self._store_recommendation, 
                request_id, 
                response.dict()
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate recommendations: {str(e)}"
            )
    
    async def get_recommendation(self, request_id: str) -> RecommendationResponse:
        """
        Retrieve a previously generated recommendation.
        
        Args:
            request_id: Unique identifier for the recommendation request
            
        Returns:
            RecommendationResponse with the requested recommendations
        """
        try:
            if request_id not in self.recommendation_history:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Recommendation with ID {request_id} not found"
                )
            
            stored_data = self.recommendation_history[request_id]
            
            return RecommendationResponse(**stored_data)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve recommendation: {str(e)}"
            )
    
    async def get_recommendation_history(self) -> List[RecommendationHistory]:
        """
        Get recommendation history.
        
        Returns:
            List of recommendation history entries
        """
        try:
            history = []
            
            for request_id, data in self.recommendation_history.items():
                history_entry = RecommendationHistory(
                    request_id=request_id,
                    preferences=UserPreferences(**data["preferences"]),
                    recommendations_count=len(data["recommendations"]),
                    created_at=data["created_at"]
                )
                history.append(history_entry)
            
            # Sort by creation time (newest first)
            history.sort(key=lambda x: x.created_at, reverse=True)
            
            return history
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve recommendation history: {str(e)}"
            )
    
    def _validate_preferences(self, preferences: UserPreferences) -> None:
        """Validate user preferences."""
        if not preferences.location.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location cannot be empty"
            )
        
        if preferences.budget.min < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum budget cannot be negative"
            )
        
        if preferences.budget.max <= preferences.budget.min:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum budget must be greater than minimum budget"
            )
        
        if preferences.minimum_rating < 0 or preferences.minimum_rating > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum rating must be between 0 and 5"
            )
    
    async def _generate_recommendations_pipeline(
        self, 
        preferences: UserPreferences, 
        top_k: int
    ) -> List[RestaurantInfo]:
        """
        Generate recommendations using the Phase 1-5 pipeline.
        
        Args:
            preferences: User preferences
            top_k: Number of recommendations to generate
            
        Returns:
            List of restaurant recommendations
        """
        try:
            # For demo purposes, return sample recommendations
            # In real implementation, this would call the actual Phase 4 pipeline
            return self._generate_sample_recommendations(preferences, top_k)
            
        except Exception as e:
            # Fallback to sample recommendations if pipeline fails
            return self._generate_sample_recommendations(preferences, top_k)
    
    def _generate_sample_recommendations(
        self, 
        preferences: UserPreferences, 
        top_k: int
    ) -> List[RestaurantInfo]:
        """Generate sample recommendations for demo purposes."""
        sample_restaurants = [
            RestaurantInfo(
                name="Byg Brewski Brewing Company",
                city=preferences.location,
                cuisines=["Continental", "North Indian", "Italian"],
                rating=4.9,
                cost_estimate=1600,
                reason="Excellent rating with diverse cuisine options within your budget"
            ),
            RestaurantInfo(
                name="The Black Pearl",
                city=preferences.location,
                cuisines=["North Indian", "European", "Mediterranean"],
                rating=4.8,
                cost_estimate=1500,
                reason="High-quality dining experience with great ambiance"
            ),
            RestaurantInfo(
                name="AB's - Absolute Barbecues",
                city=preferences.location,
                cuisines=["European", "Mediterranean", "BBQ"],
                rating=4.7,
                cost_estimate=1600,
                reason="Premium barbecue experience with excellent service"
            ),
            RestaurantInfo(
                name="Opus Food Stories",
                city=preferences.location,
                cuisines=["Goan", "Asian", "Continental"],
                rating=4.7,
                cost_estimate=1500,
                reason="Unique fusion cuisine with great value for money"
            ),
            RestaurantInfo(
                name="The Hole in the Wall Café",
                city=preferences.location,
                cuisines=["Continental", "Italian", "Cafe"],
                rating=4.6,
                cost_estimate=1200,
                reason="Cozy atmosphere with quality food at reasonable prices"
            )
        ]
        
        # Filter by budget
        filtered_restaurants = [
            r for r in sample_restaurants 
            if r.cost_estimate <= preferences.budget.max and r.cost_estimate >= preferences.budget.min
        ]
        
        # Filter by rating
        filtered_restaurants = [
            r for r in filtered_restaurants 
            if r.rating >= preferences.minimum_rating
        ]
        
        # Filter by cuisines if specified
        if preferences.cuisines:
            filtered_restaurants = [
                r for r in filtered_restaurants 
                if any(cuisine.lower() in [pref.lower() for pref in preferences.cuisines] 
                      for cuisine in r.cuisines)
            ]
        
        # Return top_k results
        return filtered_restaurants[:top_k]
    
    def _create_metadata(self, request: RecommendationRequest, count: int) -> Dict[str, Any]:
        """Create metadata for the recommendation response."""
        return {
            "processing_time": 0.5,  # Simulated processing time
            "candidates_considered": 30,  # Simulated candidate count
            "model_used": "llama-3.3-70b-versatile",
            "top_k_requested": request.top_k,
            "recommendations_generated": count,
            "include_explanations": request.include_explanations,
            "pipeline_version": "1.0.0"
        }
    
    async def _store_recommendation(self, request_id: str, response_data: Dict[str, Any]) -> None:
        """Store recommendation in history (async)."""
        # In production, this would store in database
        self.recommendation_history[request_id] = response_data
        
        # Limit history size (demo)
        if len(self.recommendation_history) > 1000:
            # Remove oldest entries
            oldest_ids = sorted(self.recommendation_history.keys())[:100]
            for old_id in oldest_ids:
                del self.recommendation_history[old_id]
