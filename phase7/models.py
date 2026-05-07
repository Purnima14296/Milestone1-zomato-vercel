"""
Phase 7 API Models: Pydantic models for request/response validation.

This module defines the data models used by the FastAPI application for
request validation, response serialization, and type safety.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class BudgetRange(BaseModel):
    """Budget range model."""
    min: float = Field(ge=0, description="Minimum budget")
    max: float = Field(gt=0, description="Maximum budget")
    
    @validator('max')
    def max_greater_than_min(cls, v, values):
        if 'min' in values and v <= values['min']:
            raise ValueError('max must be greater than min')
        return v


class UserPreferences(BaseModel):
    """User preferences model."""
    location: str = Field(..., description="Preferred location")
    budget: BudgetRange = Field(..., description="Budget range")
    minimum_rating: float = Field(ge=0, le=5, description="Minimum rating")
    cuisines: List[str] = Field(default=[], description="Preferred cuisines")
    additional_preferences: Optional[str] = Field(None, description="Additional preferences")


class RestaurantInfo(BaseModel):
    """Restaurant information model."""
    name: str = Field(..., description="Restaurant name")
    city: str = Field(..., description="Restaurant city")
    cuisines: List[str] = Field(..., description="Available cuisines")
    rating: float = Field(ge=0, le=5, description="Restaurant rating")
    cost_estimate: float = Field(ge=0, description="Estimated cost")
    reason: str = Field(..., description="Recommendation reason")


class RecommendationRequest(BaseModel):
    """Recommendation request model."""
    preferences: UserPreferences = Field(..., description="User preferences")
    top_k: Optional[int] = Field(default=5, ge=1, le=20, description="Number of recommendations")
    include_explanations: Optional[bool] = Field(default=True, description="Include AI explanations")


class RecommendationResponse(BaseModel):
    """Recommendation response model."""
    request_id: str = Field(..., description="Unique request identifier")
    preferences: UserPreferences = Field(..., description="User preferences used")
    recommendations: List[RestaurantInfo] = Field(..., description="Generated recommendations")
    metadata: Dict[str, Any] = Field(..., description="Request metadata")
    created_at: datetime = Field(..., description="Timestamp")


class RecommendationHistory(BaseModel):
    """Recommendation history model."""
    request_id: str = Field(..., description="Request identifier")
    preferences: UserPreferences = Field(..., description="User preferences")
    recommendations_count: int = Field(..., description="Number of recommendations")
    created_at: datetime = Field(..., description="Creation timestamp")


class RestaurantSearchRequest(BaseModel):
    """Restaurant search request model."""
    location: Optional[str] = Field(None, description="Filter by location")
    cuisine: Optional[str] = Field(None, description="Filter by cuisine")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating filter")
    max_cost: Optional[float] = Field(None, ge=0, description="Maximum cost filter")
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Result limit")
    offset: Optional[int] = Field(default=0, ge=0, description="Result offset")


class RestaurantSearchResponse(BaseModel):
    """Restaurant search response model."""
    restaurants: List[RestaurantInfo] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of results")
    limit: int = Field(..., description="Results limit")
    offset: int = Field(..., description="Results offset")


class PreferenceValidationRequest(BaseModel):
    """Preference validation request model."""
    preferences: UserPreferences = Field(..., description="Preferences to validate")


class ValidationError(BaseModel):
    """Validation error model."""
    field: str = Field(..., description="Field with error")
    message: str = Field(..., description="Error message")
    severity: str = Field(..., description="Error severity")


class PreferenceValidationResponse(BaseModel):
    """Preference validation response model."""
    valid: bool = Field(..., description="Validation result")
    errors: List[ValidationError] = Field(default=[], description="Validation errors")
    warnings: List[ValidationError] = Field(default=[], description="Validation warnings")
    suggestions: List[str] = Field(default=[], description="Improvement suggestions")


class HealthStatus(str, Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


class ComponentHealth(BaseModel):
    """Component health model."""
    name: str = Field(..., description="Component name")
    status: HealthStatus = Field(..., description="Health status")
    response_time: float = Field(..., description="Response time in seconds")
    message: Optional[str] = Field(None, description="Status message")
    details: Dict[str, Any] = Field(default={}, description="Additional details")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: HealthStatus = Field(..., description="Overall system health")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")
    components: List[ComponentHealth] = Field(..., description="Component health status")
    uptime: float = Field(..., description="System uptime in seconds")


class SystemMetrics(BaseModel):
    """System metrics model."""
    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage percentage")
    disk_usage: float = Field(..., description="Disk usage percentage")
    active_requests: int = Field(..., description="Number of active requests")
    total_requests: int = Field(..., description="Total requests processed")
    avg_response_time: float = Field(..., description="Average response time")
    error_rate: float = Field(..., description="Error rate percentage")


class QualityMetrics(BaseModel):
    """Quality metrics model."""
    constraint_satisfaction: float = Field(..., description="Constraint satisfaction rate")
    diversity_score: float = Field(..., description="Diversity score")
    avg_quality_score: float = Field(..., description="Average quality score")
    total_recommendations: int = Field(..., description="Total recommendations generated")


class MetricsResponse(BaseModel):
    """Metrics response model."""
    timestamp: datetime = Field(..., description="Metrics timestamp")
    system: SystemMetrics = Field(..., description="System metrics")
    quality: QualityMetrics = Field(..., description="Quality metrics")
    period_hours: int = Field(..., description="Metrics period in hours")


class SystemMetadata(BaseModel):
    """System metadata model."""
    version: str = Field(..., description="API version")
    description: str = Field(..., description="System description")
    total_restaurants: int = Field(..., description="Total restaurants in database")
    total_recommendations: int = Field(..., description="Total recommendations generated")
    supported_cuisines: List[str] = Field(..., description="Supported cuisines")
    supported_locations: List[str] = Field(..., description="Supported locations")
    features: List[str] = Field(..., description="Available features")


class MetadataResponse(BaseModel):
    """Metadata response model."""
    system: SystemMetadata = Field(..., description="System metadata")
    timestamp: datetime = Field(..., description="Response timestamp")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request identifier")


class SuccessResponse(BaseModel):
    """Success response model."""
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: datetime = Field(..., description="Response timestamp")
