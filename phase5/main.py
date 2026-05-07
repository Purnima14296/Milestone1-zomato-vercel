"""
Phase 5 Main Entry Point: Standalone runner for the presentation layer.

This module provides a standalone entry point that can be run directly
without relative imports.
"""

import sys
from pathlib import Path

# Add the phase5 directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from renderer import RecommendationRenderer, load_recommendations, RestaurantDisplay
from ux_enhancements import (
    RecommendationEnhancer, 
    SortOrder, 
    FilterType, 
    FilterCriteria, 
    SortCriteria
)
import argparse
import json


def build_parser() -> argparse.ArgumentParser:
    """Build the comprehensive command-line argument parser."""
    p = argparse.ArgumentParser(
        description="Phase 5: Presentation Layer - Enhanced restaurant recommendations display"
    )
    
    # Input/Output options
    p.add_argument(
        "--input",
        default="storage/recommendations.json",
        help="Path to Phase 4 recommendations JSON file"
    )
    p.add_argument(
        "--preferences",
        default="test_preferences.json",
        help="Path to user preferences JSON file"
    )
    p.add_argument(
        "--format",
        choices=["console", "json", "markdown", "enhanced"],
        default="enhanced",
        help="Output format for recommendations"
    )
    p.add_argument(
        "--output",
        help="Output file path (if not specified, prints to stdout)"
    )
    p.add_argument(
        "--max-width",
        type=int,
        default=80,
        help="Maximum line width for console output"
    )
    
    # Sorting options
    p.add_argument(
        "--sort",
        choices=["rank", "rating_high", "rating_low", "cost_high", "cost_low", "name_asc", "name_desc"],
        default="rank",
        help="Sort recommendations by specified field"
    )
    
    # Filtering options
    p.add_argument(
        "--filter-rating",
        type=float,
        help="Filter by minimum rating"
    )
    p.add_argument(
        "--filter-cost",
        type=float,
        help="Filter by maximum cost"
    )
    p.add_argument(
        "--filter-cuisine",
        help="Filter by cuisine (partial match)"
    )
    p.add_argument(
        "--filter-location",
        help="Filter by location (partial match)"
    )
    
    # Display options
    p.add_argument(
        "--top-k",
        type=int,
        help="Limit to top K recommendations"
    )
    p.add_argument(
        "--compare",
        nargs="+",
        type=int,
        help="Compare specific restaurants by index (e.g., --compare 0 1 2)"
    )
    p.add_argument(
        "--show-suggestions",
        action="store_true",
        help="Show preference refinement suggestions"
    )
    p.add_argument(
        "--show-filters",
        action="store_true",
        help="Show available filter suggestions"
    )
    
    return p


def apply_filters(
    restaurants: list[RestaurantDisplay], 
    args: argparse.Namespace
) -> list[RestaurantDisplay]:
    """Apply command-line filters to restaurants."""
    enhancer = RecommendationEnhancer()
    filters = []
    
    if args.filter_rating:
        filters.append(FilterCriteria(
            FilterType.RATING_MIN,
            args.filter_rating,
            f"Rating ≥ {args.filter_rating}"
        ))
    
    if args.filter_cost:
        filters.append(FilterCriteria(
            FilterType.COST_MAX,
            args.filter_cost,
            f"Cost ≤ ₹{args.filter_cost}"
        ))
    
    if args.filter_cuisine:
        filters.append(FilterCriteria(
            FilterType.CUISINE,
            args.filter_cuisine,
            f"Cuisine: {args.filter_cuisine}"
        ))
    
    if args.filter_location:
        filters.append(FilterCriteria(
            FilterType.LOCATION,
            args.filter_location,
            f"Location: {args.filter_location}"
        ))
    
    return enhancer.filter_recommendations(restaurants, filters)


def render_enhanced_output(
    restaurants: list[RestaurantDisplay],
    args: argparse.Namespace,
    renderer: RecommendationRenderer,
    enhancer: RecommendationEnhancer,
    preferences: dict
) -> str:
    """Render enhanced output with UX features."""
    lines = []
    
    # Header
    lines.append("=" * args.max_width)
    lines.append("🍽️  ENHANCED RESTAURANT RECOMMENDATIONS")
    lines.append("=" * args.max_width)
    lines.append("")
    
    # Applied filters
    filters = []
    if args.filter_rating:
        filters.append(f"Rating ≥ {args.filter_rating}")
    if args.filter_cost:
        filters.append(f"Cost ≤ ₹{args.filter_cost}")
    if args.filter_cuisine:
        filters.append(f"Cuisine: {args.filter_cuisine}")
    if args.filter_location:
        filters.append(f"Location: {args.filter_location}")
    
    if filters:
        lines.append("🔍 Applied Filters:")
        for f in filters:
            lines.append(f"   • {f}")
        lines.append("")
    
    # Sort information
    sort_desc = {
        "rank": "Original AI Ranking",
        "rating_high": "Rating (High to Low)",
        "rating_low": "Rating (Low to High)",
        "cost_high": "Cost (High to Low)",
        "cost_low": "Cost (Low to High)",
        "name_asc": "Name (A to Z)",
        "name_desc": "Name (Z to A)"
    }
    lines.append(f"📊 Sorted by: {sort_desc.get(args.sort, 'Unknown')}")
    lines.append("")
    
    # Restaurant recommendations
    console_output = renderer.render_console(restaurants)
    lines.append(console_output)
    
    # Comparison if requested
    if args.compare:
        lines.append("")
        lines.append("=" * args.max_width)
        lines.append("🔍 RESTAURANT COMPARISON")
        lines.append("=" * args.max_width)
        lines.append("")
        
        comparison = enhancer.compare_restaurants(restaurants, args.compare)
        if "error" in comparison:
            lines.append(f"❌ {comparison['error']}")
        else:
            lines.append("📊 Comparison Results:")
            for i, restaurant in enumerate(comparison["restaurants"]):
                lines.append(f"   {i+1}. {restaurant['name']} (Rank #{restaurant['rank']})")
                lines.append(f"      Rating: {restaurant['rating']}/5.0 | Cost: ₹{restaurant['cost']:,.0f}")
                lines.append(f"      Cuisines: {', '.join(restaurant['cuisines'][:3])}")
                lines.append("")
            
            analysis = comparison["analysis"]
            lines.append("📈 Analysis:")
            lines.append(f"   • Highest Rated: {analysis['highest_rated']}")
            lines.append(f"   • Lowest Cost: {analysis['lowest_cost']}")
            lines.append(f"   • Average Rating: {analysis['avg_rating']:.1f}/5.0")
            lines.append(f"   • Average Cost: ₹{analysis['avg_cost']:,.0f}")
            lines.append(f"   • Rating Range: {analysis['rating_range']:.1f}")
            lines.append(f"   • Cost Range: ₹{analysis['cost_range']:,.0f}")
    
    # Filter suggestions if requested
    if args.show_filters:
        lines.append("")
        lines.append("=" * args.max_width)
        lines.append("💡 FILTER SUGGESTIONS")
        lines.append("=" * args.max_width)
        lines.append("")
        
        suggestions = enhancer.get_filter_suggestions(restaurants)
        if suggestions:
            lines.append("🔍 Available Filters:")
            for suggestion in suggestions:
                lines.append(f"   • {suggestion.description}")
        else:
            lines.append("No filter suggestions available.")
    
    # Preference refinement suggestions if requested
    if args.show_suggestions:
        lines.append("")
        lines.append("=" * args.max_width)
        lines.append("💡 PREFERENCE REFINEMENT SUGGESTIONS")
        lines.append("=" * args.max_width)
        lines.append("")
        
        refinements = enhancer.get_preference_refinements(restaurants, preferences)
        if refinements:
            lines.append("🎯 Suggestions for Better Recommendations:")
            for refinement in refinements:
                lines.append(f"   • {refinement}")
        else:
            lines.append("No refinement suggestions available.")
    
    return "\n".join(lines)


def load_preferences(preferences_path: str) -> dict:
    """Load user preferences from JSON file."""
    try:
        with open(preferences_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def main(argv: list[str] | None = None) -> int:
    """Main entry point for Phase 5."""
    args = build_parser().parse_args(argv)
    
    # Check if input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        print("Run Phase 4 first to generate recommendations.", file=sys.stderr)
        return 1
    
    try:
        # Load data
        recommendations = load_recommendations(str(input_path))
        preferences = load_preferences(args.preferences)
        
        if not recommendations:
            print("No recommendations found in the input file.", file=sys.stderr)
            return 1
        
        # Create renderer and enhancer
        renderer = RecommendationRenderer(max_width=args.max_width)
        enhancer = RecommendationEnhancer()
        
        # Parse recommendations
        restaurant_displays = renderer.parse_recommendations(recommendations)
        
        # Apply sorting
        sort_order_map = {
            "rank": SortOrder.RANK,
            "rating_high": SortOrder.RATING_HIGH,
            "rating_low": SortOrder.RATING_LOW,
            "cost_high": SortOrder.COST_HIGH,
            "cost_low": SortOrder.COST_LOW,
            "name_asc": SortOrder.NAME_ASC,
            "name_desc": SortOrder.NAME_DESC
        }
        sort_order = sort_order_map.get(args.sort, SortOrder.RANK)
        restaurant_displays = enhancer.sort_recommendations(restaurant_displays, sort_order)
        
        # Apply filters
        restaurant_displays = apply_filters(restaurant_displays, args)
        
        # Limit to top K if specified
        if args.top_k and args.top_k > 0:
            restaurant_displays = restaurant_displays[:args.top_k]
        
        # Generate output
        if args.format == "console":
            output = renderer.render_console(restaurant_displays)
        elif args.format == "json":
            output = renderer.render_json(restaurant_displays)
        elif args.format == "markdown":
            output = renderer.render_markdown(restaurant_displays)
        elif args.format == "enhanced":
            output = render_enhanced_output(
                restaurant_displays, args, renderer, enhancer, preferences
            )
        else:
            output = renderer.render_console(restaurant_displays)
        
        # Output to file or stdout
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Recommendations written to: {args.output}")
        else:
            print(output)
        
        return 0
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
