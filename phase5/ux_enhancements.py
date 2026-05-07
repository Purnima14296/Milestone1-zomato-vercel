"""
Phase 5 UX Enhancements: Additional user experience features.

This module provides optional enhancements for better user interaction
with restaurant recommendations including sorting, filtering, and
preference refinement capabilities.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from renderer import RestaurantDisplay


class SortOrder(Enum):
    """Enumeration for sorting options."""
    RANK = "rank"
    RATING_HIGH = "rating_high"
    RATING_LOW = "rating_low"
    COST_HIGH = "cost_high"
    COST_LOW = "cost_low"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"


class FilterType(Enum):
    """Enumeration for filtering options."""
    NONE = "none"
    RATING_MIN = "rating_min"
    COST_MAX = "cost_max"
    CUISINE = "cuisine"
    LOCATION = "location"


@dataclass
class FilterCriteria:
    """Criteria for filtering recommendations."""
    filter_type: FilterType
    value: Any
    description: str


@dataclass
class SortCriteria:
    """Criteria for sorting recommendations."""
    sort_order: SortOrder
    description: str


class RecommendationEnhancer:
    """
    Provides UX enhancements for restaurant recommendations.
    
    Features include:
    - Multiple sorting options
    - Filtering capabilities
    - Preference refinement suggestions
    - Comparison tools
    """
    
    def __init__(self):
        self.current_filters: List[FilterCriteria] = []
        self.current_sort: Optional[SortCriteria] = None
    
    def sort_recommendations(
        self, 
        restaurants: List[RestaurantDisplay], 
        sort_order: SortOrder
    ) -> List[RestaurantDisplay]:
        """
        Sort restaurants based on the specified criteria.
        
        Args:
            restaurants: List of restaurants to sort
            sort_order: Sorting criteria
            
        Returns:
            Sorted list of restaurants
        """
        if sort_order == SortOrder.RANK:
            return sorted(restaurants, key=lambda x: x.rank)
        elif sort_order == SortOrder.RATING_HIGH:
            return sorted(restaurants, key=lambda x: x.rating, reverse=True)
        elif sort_order == SortOrder.RATING_LOW:
            return sorted(restaurants, key=lambda x: x.rating)
        elif sort_order == SortOrder.COST_HIGH:
            return sorted(restaurants, key=lambda x: x.cost_estimate, reverse=True)
        elif sort_order == SortOrder.COST_LOW:
            return sorted(restaurants, key=lambda x: x.cost_estimate)
        elif sort_order == SortOrder.NAME_ASC:
            return sorted(restaurants, key=lambda x: x.name.lower())
        elif sort_order == SortOrder.NAME_DESC:
            return sorted(restaurants, key=lambda x: x.name.lower(), reverse=True)
        else:
            return restaurants
    
    def filter_recommendations(
        self, 
        restaurants: List[RestaurantDisplay], 
        filters: List[FilterCriteria]
    ) -> List[RestaurantDisplay]:
        """
        Filter restaurants based on the specified criteria.
        
        Args:
            restaurants: List of restaurants to filter
            filters: List of filter criteria
            
        Returns:
            Filtered list of restaurants
        """
        filtered = restaurants.copy()
        
        for filter_criteria in filters:
            if filter_criteria.filter_type == FilterType.RATING_MIN:
                min_rating = filter_criteria.value
                filtered = [r for r in filtered if r.rating >= min_rating]
            elif filter_criteria.filter_type == FilterType.COST_MAX:
                max_cost = filter_criteria.value
                filtered = [r for r in filtered if r.cost_estimate <= max_cost]
            elif filter_criteria.filter_type == FilterType.CUISINE:
                target_cuisine = filter_criteria.value.lower()
                filtered = [r for r in filtered 
                           if any(target_cuisine in cuisine.lower() 
                                for cuisine in r.cuisines)]
            elif filter_criteria.filter_type == FilterType.LOCATION:
                target_location = filter_criteria.value.lower()
                filtered = [r for r in filtered 
                           if target_location in r.city.lower()]
        
        return filtered
    
    def get_available_sort_options(self) -> List[SortCriteria]:
        """Get all available sorting options."""
        return [
            SortCriteria(SortOrder.RANK, "Original ranking (AI recommended)"),
            SortCriteria(SortOrder.RATING_HIGH, "Rating (high to low)"),
            SortCriteria(SortOrder.RATING_LOW, "Rating (low to high)"),
            SortCriteria(SortOrder.COST_HIGH, "Cost (high to low)"),
            SortCriteria(SortOrder.COST_LOW, "Cost (low to high)"),
            SortCriteria(SortOrder.NAME_ASC, "Name (A to Z)"),
            SortCriteria(SortOrder.NAME_DESC, "Name (Z to A)"),
        ]
    
    def get_filter_suggestions(
        self, 
        restaurants: List[RestaurantDisplay]
    ) -> List[FilterCriteria]:
        """
        Generate filter suggestions based on the current recommendations.
        
        Args:
            restaurants: List of current recommendations
            
        Returns:
            List of suggested filter criteria
        """
        suggestions = []
        
        # Rating filters
        ratings = sorted(set(r.rating for r in restaurants))
        if len(ratings) > 1:
            suggestions.append(
                FilterCriteria(
                    FilterType.RATING_MIN, 
                    max(ratings) - 0.5,
                    f"High rating (≥{max(ratings) - 0.5:.1f})"
                )
            )
            suggestions.append(
                FilterCriteria(
                    FilterType.RATING_MIN, 
                    4.5,
                    "Excellent rating (≥4.5)"
                )
            )
        
        # Cost filters
        costs = sorted(set(r.cost_estimate for r in restaurants))
        if len(costs) > 1:
            median_cost = costs[len(costs)//2]
            suggestions.append(
                FilterCriteria(
                    FilterType.COST_MAX,
                    median_cost,
                    f"Budget-friendly (≤₹{median_cost:,.0f})"
                )
            )
        
        # Cuisine filters
        all_cuisines = set()
        for r in restaurants:
            for cuisine in r.cuisines:
                if isinstance(cuisine, str):
                    clean_cuisine = cuisine.strip("'\"[]")
                    if clean_cuisine:
                        all_cuisines.add(clean_cuisine)
        
        popular_cuisines = [c for c in all_cuisines if c][:3]  # Top 3
        for cuisine in popular_cuisines:
            suggestions.append(
                FilterCriteria(
                    FilterType.CUISINE,
                    cuisine,
                    f"Cuisine: {cuisine}"
                )
            )
        
        return suggestions
    
    def compare_restaurants(
        self, 
        restaurants: List[RestaurantDisplay], 
        indices: List[int]
    ) -> Dict[str, Any]:
        """
        Compare selected restaurants side by side.
        
        Args:
            restaurants: List of restaurants
            indices: List of restaurant indices to compare
            
        Returns:
            Comparison data structure
        """
        selected = [restaurants[i] for i in indices if 0 <= i < len(restaurants)]
        
        if len(selected) < 2:
            return {"error": "Need at least 2 restaurants to compare"}
        
        comparison = {
            "restaurants": [],
            "analysis": {}
        }
        
        # Add restaurant details
        for r in selected:
            comparison["restaurants"].append({
                "rank": r.rank,
                "name": r.name,
                "rating": r.rating,
                "cost": r.cost_estimate,
                "cuisines": r.cuisines,
                "city": r.city
            })
        
        # Analysis
        ratings = [r.rating for r in selected]
        costs = [r.cost_estimate for r in selected]
        
        comparison["analysis"] = {
            "highest_rated": max(selected, key=lambda x: x.rating).name,
            "lowest_cost": min(selected, key=lambda x: x.cost_estimate).name,
            "avg_rating": sum(ratings) / len(ratings),
            "avg_cost": sum(costs) / len(costs),
            "rating_range": max(ratings) - min(ratings),
            "cost_range": max(costs) - min(costs)
        }
        
        return comparison
    
    def get_preference_refinements(
        self, 
        restaurants: List[RestaurantDisplay],
        original_preferences: Dict[str, Any]
    ) -> List[str]:
        """
        Suggest preference refinements based on current recommendations.
        
        Args:
            restaurants: Current recommendations
            original_preferences: Original user preferences
            
        Returns:
            List of refinement suggestions
        """
        suggestions = []
        
        if not restaurants:
            return ["No recommendations available for refinement analysis"]
        
        # Analyze rating distribution
        ratings = [r.rating for r in restaurants]
        avg_rating = sum(ratings) / len(ratings)
        
        if avg_rating < 4.5 and original_preferences.get("minimum_rating", 0) < 4.5:
            suggestions.append("Consider increasing minimum rating to 4.5+ for higher quality options")
        
        # Analyze cost distribution
        costs = [r.cost_estimate for r in restaurants]
        avg_cost = sum(costs) / len(costs)
        
        original_budget = original_preferences.get("budget", {})
        if isinstance(original_budget, dict):
            max_budget = original_budget.get("max", 999999)
        else:
            max_budget = original_budget
        
        if avg_cost < max_budget * 0.7:
            suggestions.append("You have room in your budget - consider increasing it for more premium options")
        elif avg_cost > max_budget * 0.9:
            suggestions.append("Most options are near your budget limit - consider increasing budget for more choices")
        
        # Analyze cuisine diversity
        all_cuisines = set()
        for r in restaurants:
            for cuisine in r.cuisines:
                if isinstance(cuisine, str):
                    clean_cuisine = cuisine.strip("'\"[]")
                    if clean_cuisine:
                        all_cuisines.add(clean_cuisine)
        
        if len(all_cuisines) < 3:
            suggestions.append("Limited cuisine variety - consider being more open to different cuisines")
        
        return suggestions
