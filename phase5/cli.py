"""
Phase 5 CLI: Command-line interface for the presentation layer.

This module provides a command-line interface to render and display
restaurant recommendations from Phase 4 output.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .renderer import RecommendationRenderer, load_recommendations


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    p = argparse.ArgumentParser(
        description="Phase 5: Presentation Layer - Display restaurant recommendations"
    )
    p.add_argument(
        "--input",
        default="storage/recommendations.json",
        help="Path to Phase 4 recommendations JSON file"
    )
    p.add_argument(
        "--format",
        choices=["console", "json", "markdown"],
        default="console",
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
    p.add_argument(
        "--sort-by",
        choices=["rank", "rating", "cost", "name"],
        default="rank",
        help="Sort recommendations by specified field"
    )
    p.add_argument(
        "--top-k",
        type=int,
        help="Limit to top K recommendations"
    )
    return p


def sort_recommendations(recommendations, sort_by: str):
    """Sort recommendations by the specified field."""
    if sort_by == "rank":
        return sorted(recommendations, key=lambda x: x.get("rank", 999))
    elif sort_by == "rating":
        return sorted(recommendations, key=lambda x: x.get("rating", 0), reverse=True)
    elif sort_by == "cost":
        return sorted(recommendations, key=lambda x: x.get("cost_estimate", 999999))
    elif sort_by == "name":
        return sorted(recommendations, key=lambda x: x.get("restaurant_name", ""))
    else:
        return recommendations


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    args = build_parser().parse_args(argv)
    
    # Check if input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        print("Run Phase 4 first to generate recommendations.", file=sys.stderr)
        return 1
    
    try:
        # Load recommendations from Phase 4
        recommendations = load_recommendations(str(input_path))
        
        if not recommendations:
            print("No recommendations found in the input file.", file=sys.stderr)
            return 1
        
        # Sort recommendations
        recommendations = sort_recommendations(recommendations, args.sort_by)
        
        # Limit to top K if specified
        if args.top_k and args.top_k > 0:
            recommendations = recommendations[:args.top_k]
        
        # Create renderer
        renderer = RecommendationRenderer(max_width=args.max_width)
        
        # Parse recommendations into display objects
        restaurant_displays = renderer.parse_recommendations(recommendations)
        
        # Render in requested format
        if args.format == "console":
            output = renderer.render_console(restaurant_displays)
        elif args.format == "json":
            output = renderer.render_json(restaurant_displays)
        elif args.format == "markdown":
            output = renderer.render_markdown(restaurant_displays)
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
