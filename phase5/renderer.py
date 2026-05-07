"""
Phase 5 Renderer: User-friendly presentation of restaurant recommendations.

This module provides rendering capabilities for displaying top K restaurant
recommendations with detailed information and AI-generated explanations.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List
from dataclasses import dataclass


@dataclass
class RestaurantDisplay:
    """Structured representation of a restaurant for display."""
    rank: int
    name: str
    cuisines: List[str]
    rating: float
    cost_estimate: float
    city: str
    ai_explanation: str


class RecommendationRenderer:
    """
    Renders restaurant recommendations in various user-friendly formats.
    
    Supports console output, JSON, and can be extended for web/UI display.
    """
    
    def __init__(self, max_width: int = 80):
        self.max_width = max_width
    
    def parse_recommendations(self, recommendations_json: List[Dict[str, Any]]) -> List[RestaurantDisplay]:
        """
        Parse the JSON output from Phase 4 into structured display objects.
        
        Args:
            recommendations_json: List of recommendation dictionaries from Phase 4
            
        Returns:
            List of RestaurantDisplay objects ready for rendering
        """
        displays = []
        for rec in recommendations_json:
            # Handle cuisines - they might be stored as string representations of lists
            cuisines_raw = rec.get("cuisines", [])
            if isinstance(cuisines_raw, str):
                try:
                    # Try to parse if it looks like a Python list string
                    if cuisines_raw.startswith("[") and cuisines_raw.endswith("]"):
                        import ast
                        cuisines = ast.literal_eval(cuisines_raw)
                    else:
                        cuisines = [cuisines_raw]
                except:
                    cuisines = [cuisines_raw]
            elif isinstance(cuisines_raw, list):
                cuisines = cuisines_raw
            else:
                cuisines = []
            
            display = RestaurantDisplay(
                rank=rec.get("rank", 0),
                name=rec.get("restaurant_name", "Unknown"),
                cuisines=cuisines,
                rating=rec.get("rating", 0.0),
                cost_estimate=rec.get("cost_estimate", 0.0),
                city=rec.get("city", "Unknown"),
                ai_explanation=rec.get("reason", "No explanation available")
            )
            displays.append(display)
        
        return displays
    
    def render_console(self, restaurants: List[RestaurantDisplay]) -> str:
        """
        Render recommendations as a formatted console output.
        
        Args:
            restaurants: List of RestaurantDisplay objects
            
        Returns:
            Formatted string for console display
        """
        if not restaurants:
            return "No restaurants to display."
        
        lines = []
        lines.append("=" * self.max_width)
        lines.append("RESTAURANT RECOMMENDATIONS")
        lines.append("=" * self.max_width)
        lines.append("")
        
        for restaurant in restaurants:
            # Header with rank and name
            header = f"Rank {restaurant.rank}. {restaurant.name}"
            lines.append(header)
            lines.append("-" * min(len(header), self.max_width))
            
            # Restaurant details
            lines.append(f"Location: {restaurant.city}")
            lines.append(f"Rating: {restaurant.rating}/5.0")
            lines.append(f"Cost: ${restaurant.cost_estimate:,.0f}")
            
            # Cuisines
            if restaurant.cuisines:
                # Clean up cuisine strings and format them
                cleaned_cuisines = []
                for cuisine in restaurant.cuisines:
                    if isinstance(cuisine, str):
                        # Remove quotes and brackets if present
                        clean = cuisine.strip("'\"[]")
                        if clean and clean not in cleaned_cuisines:
                            cleaned_cuisines.append(clean)
                
                if cleaned_cuisines:
                    cuisines_str = ", ".join(cleaned_cuisines[:5])  # Limit to first 5
                    if len(cleaned_cuisines) > 5:
                        cuisines_str += f" (+{len(cleaned_cuisines)-5} more)"
                    lines.append(f"Cuisines: {cuisines_str}")
            
            # AI explanation with word wrap
            lines.append("")
            lines.append("Why we recommend this:")
            explanation_lines = self._wrap_text(restaurant.ai_explanation, indent="    ")
            lines.extend(explanation_lines)
            lines.append("")
            lines.append("")
        
        # Summary
        lines.append("=" * self.max_width)
        lines.append(f"Summary: {len(restaurants)} recommendations")
        avg_rating = sum(r.rating for r in restaurants) / len(restaurants)
        avg_cost = sum(r.cost_estimate for r in restaurants) / len(restaurants)
        lines.append(f"Average Rating: {avg_rating:.1f}/5.0")
        lines.append(f"Average Cost: ${avg_cost:,.0f}")
        lines.append("=" * self.max_width)
        
        return "\n".join(lines)
    
    def render_console_simple(self, restaurants: List[RestaurantDisplay]) -> str:
        """
        Render recommendations as a simple console output without Unicode characters.
        
        Args:
            restaurants: List of RestaurantDisplay objects
            
        Returns:
            Formatted string for console display
        """
        return self.render_console(restaurants)
    
    def render_json(self, restaurants: List[RestaurantDisplay]) -> str:
        """
        Render recommendations as clean JSON output.
        
        Args:
            restaurants: List of RestaurantDisplay objects
            
        Returns:
            JSON string representation
        """
        data = []
        for restaurant in restaurants:
            item = {
                "rank": restaurant.rank,
                "restaurant_name": restaurant.name,
                "city": restaurant.city,
                "rating": restaurant.rating,
                "cost_estimate": restaurant.cost_estimate,
                "cuisines": restaurant.cuisines,
                "ai_explanation": restaurant.ai_explanation
            }
            data.append(item)
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def render_markdown(self, restaurants: List[RestaurantDisplay]) -> str:
        """
        Render recommendations as Markdown format.
        
        Args:
            restaurants: List of RestaurantDisplay objects
            
        Returns:
            Markdown string representation
        """
        if not restaurants:
            return "No restaurants to display."
        
        lines = []
        lines.append("# 🍽️ Restaurant Recommendations")
        lines.append("")
        
        for restaurant in restaurants:
            lines.append(f"## 🥇 Rank {restaurant.rank}: {restaurant.name}")
            lines.append("")
            
            # Details table
            lines.append("| Detail | Information |")
            lines.append("|--------|-------------|")
            lines.append(f"| 📍 Location | {restaurant.city} |")
            lines.append(f"| ⭐ Rating | {restaurant.rating}/5.0 |")
            lines.append(f"| 💰 Cost | ₹{restaurant.cost_estimate:,.0f} |")
            
            if restaurant.cuisines:
                cleaned_cuisines = []
                for cuisine in restaurant.cuisines:
                    if isinstance(cuisine, str):
                        clean = cuisine.strip("'\"[]")
                        if clean and clean not in cleaned_cuisines:
                            cleaned_cuisines.append(clean)
                
                if cleaned_cuisines:
                    cuisines_str = ", ".join(cleaned_cuisines)
                    lines.append(f"| 🍜 Cuisines | {cuisines_str} |")
            
            lines.append("")
            lines.append("### 💬 AI Recommendation Reason")
            lines.append("")
            lines.append(f"> {restaurant.ai_explanation}")
            lines.append("")
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    def _wrap_text(self, text: str, indent: str = "") -> List[str]:
        """
        Wrap text to fit within max_width with optional indentation.
        
        Args:
            text: Text to wrap
            indent: String to prepend to each line
            
        Returns:
            List of wrapped lines
        """
        words = text.split()
        lines = []
        current_line = indent
        
        for word in words:
            test_line = current_line + " " + word if current_line != indent else indent + word
            if len(test_line) <= self.max_width:
                current_line = test_line
            else:
                if current_line != indent:
                    lines.append(current_line)
                current_line = indent + word
        
        if current_line != indent:
            lines.append(current_line)
        
        return lines


def load_recommendations(file_path: str) -> List[Dict[str, Any]]:
    """
    Load recommendations from the Phase 4 output JSON file.
    
    Args:
        file_path: Path to the recommendations.json file
        
    Returns:
        List of recommendation dictionaries
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
