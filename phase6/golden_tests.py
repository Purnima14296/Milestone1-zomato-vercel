"""
Phase 6 Golden Tests: Repeatable test cases for system validation.

This module provides a comprehensive set of golden test queries that
cover various scenarios and edge cases to validate system behavior
and ensure consistent performance across different user preference patterns.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List
from dataclasses import dataclass
from enum import Enum


class TestScenario(Enum):
    """Enumeration of test scenario categories."""
    BUDGET_FOCUSED = "budget_focused"
    RATING_FOCUSED = "rating_focused"
    CUISINE_SPECIFIC = "cuisine_specific"
    LOCATION_EDGE_CASES = "location_edge_cases"
    COMPLEX_PREFERENCES = "complex_preferences"
    CONSTRAINT_HEAVY = "constraint_heavy"
    MINIMAL_PREFERENCES = "minimal_preferences"
    EXTREME_VALUES = "extreme_values"


@dataclass
class GoldenTestCase:
    """Represents a single golden test case."""
    name: str
    scenario: TestScenario
    preferences: Dict[str, Any]
    expected_constraints: Dict[str, Any]
    description: str
    tags: List[str]


class GoldenTestSuite:
    """
    Comprehensive suite of golden test cases for system validation.
    
    Provides repeatable test scenarios covering various user preference
    patterns and edge cases to ensure system reliability and consistency.
    """
    
    def __init__(self):
        self.test_cases = self._generate_test_cases()
    
    def _generate_test_cases(self) -> List[GoldenTestCase]:
        """Generate comprehensive golden test cases."""
        test_cases = []
        
        # Budget-focused scenarios
        test_cases.extend([
            GoldenTestCase(
                name="low_budget_student",
                scenario=TestScenario.BUDGET_FOCUSED,
                preferences={
                    "location": "Bellandur",
                    "budget": {"min": 0, "max": 500},
                    "minimum_rating": 3.5,
                    "cuisines": [],
                    "additional_preferences": "budget-friendly, student area"
                },
                expected_constraints={
                    "max_cost": 500,
                    "min_rating": 3.5,
                    "location_match": "Bellandur"
                },
                description="Low budget student looking for affordable options",
                tags=["budget", "student", "low_cost"]
            ),
            GoldenTestCase(
                name="luxury_dining",
                scenario=TestScenario.BUDGET_FOCUSED,
                preferences={
                    "location": "Indiranagar",
                    "budget": {"min": 2000, "max": 5000},
                    "minimum_rating": 4.5,
                    "cuisines": ["Fine Dining", "Continental"],
                    "additional_preferences": "premium experience, special occasion"
                },
                expected_constraints={
                    "min_cost": 2000,
                    "max_cost": 5000,
                    "min_rating": 4.5,
                    "cuisine_match": ["Fine Dining", "Continental"]
                },
                description="High-end dining experience for special occasions",
                tags=["luxury", "fine_dining", "high_cost"]
            )
        ])
        
        # Rating-focused scenarios
        test_cases.extend([
            GoldenTestCase(
                name="quality_conscious",
                scenario=TestScenario.RATING_FOCUSED,
                preferences={
                    "location": "Koramangala",
                    "budget": {"min": 0, "max": 2000},
                    "minimum_rating": 4.8,
                    "cuisines": [],
                    "additional_preferences": "highest quality only"
                },
                expected_constraints={
                    "min_rating": 4.8,
                    "max_cost": 2000
                },
                description="User prioritizing highest ratings over other factors",
                tags=["rating", "quality", "high_standards"]
            ),
            GoldenTestCase(
                name="balanced_preferences",
                scenario=TestScenario.RATING_FOCUSED,
                preferences={
                    "location": "HSR Layout",
                    "budget": {"min": 800, "max": 1800},
                    "minimum_rating": 4.2,
                    "cuisines": ["North Indian", "Chinese"],
                    "additional_preferences": "good balance of quality and price"
                },
                expected_constraints={
                    "min_rating": 4.2,
                    "min_cost": 800,
                    "max_cost": 1800,
                    "cuisine_match": ["North Indian", "Chinese"]
                },
                description="Balanced approach between rating and budget",
                tags=["balanced", "moderate", "mixed_cuisine"]
            )
        ])
        
        # Cuisine-specific scenarios
        test_cases.extend([
            GoldenTestCase(
                name="cuisine_purist",
                scenario=TestScenario.CUISINE_SPECIFIC,
                preferences={
                    "location": "Jayanagar",
                    "budget": {"min": 0, "max": 1500},
                    "minimum_rating": 4.0,
                    "cuisines": ["South Indian"],
                    "additional_preferences": "authentic traditional South Indian only"
                },
                expected_constraints={
                    "cuisine_match": ["South Indian"],
                    "max_cost": 1500,
                    "min_rating": 4.0
                },
                description="User seeking specific cuisine type exclusively",
                tags=["cuisine_specific", "traditional", "authentic"]
            ),
            GoldenTestCase(
                name="fusion_explorer",
                scenario=TestScenario.CUISINE_SPECIFIC,
                preferences={
                    "location": "Whitefield",
                    "budget": {"min": 1000, "max": 2500},
                    "minimum_rating": 4.3,
                    "cuisines": ["Fusion", "Asian", "Continental"],
                    "additional_preferences": "innovative fusion combinations"
                },
                expected_constraints={
                    "cuisine_match": ["Fusion", "Asian", "Continental"],
                    "min_cost": 1000,
                    "max_cost": 2500,
                    "min_rating": 4.3
                },
                description="User interested in fusion and innovative cuisine",
                tags=["fusion", "innovative", "modern"]
            )
        ])
        
        # Location edge cases
        test_cases.extend([
            GoldenTestCase(
                name="remote_location",
                scenario=TestScenario.LOCATION_EDGE_CASES,
                preferences={
                    "location": "Electronic City",
                    "budget": {"min": 0, "max": 1200},
                    "minimum_rating": 3.8,
                    "cuisines": [],
                    "additional_preferences": "near tech park, lunch options"
                },
                expected_constraints={
                    "location_match": "Electronic City",
                    "max_cost": 1200,
                    "min_rating": 3.8
                },
                description="User in remote tech location with limited options",
                tags=["remote", "tech_park", "limited_options"]
            ),
            GoldenTestCase(
                name="city_center",
                scenario=TestScenario.LOCATION_EDGE_CASES,
                preferences={
                    "location": "MG Road",
                    "budget": {"min": 500, "max": 2000},
                    "minimum_rating": 4.0,
                    "cuisines": [],
                    "additional_preferences": "central location, easy access"
                },
                expected_constraints={
                    "location_match": "MG Road",
                    "min_cost": 500,
                    "max_cost": 2000,
                    "min_rating": 4.0
                },
                description="User in prime city center location",
                tags=["city_center", "prime_location", "accessible"]
            )
        ])
        
        # Complex preferences
        test_cases.extend([
            GoldenTestCase(
                name="family_dining",
                scenario=TestScenario.COMPLEX_PREFERENCES,
                preferences={
                    "location": "Marathahalli",
                    "budget": {"min": 800, "max": 2000},
                    "minimum_rating": 4.2,
                    "cuisines": ["North Indian", "Chinese", "Continental"],
                    "additional_preferences": "family-friendly, kids menu, spacious, parking"
                },
                expected_constraints={
                    "location_match": "Marathahalli",
                    "min_cost": 800,
                    "max_cost": 2000,
                    "min_rating": 4.2,
                    "cuisine_match": ["North Indian", "Chinese", "Continental"]
                },
                description="Family with multiple requirements and constraints",
                tags=["family", "multiple_constraints", "spacious"]
            ),
            GoldenTestCase(
                name="health_conscious",
                scenario=TestScenario.COMPLEX_PREFERENCES,
                preferences={
                    "location": "Indiranagar",
                    "budget": {"min": 600, "max": 1800},
                    "minimum_rating": 4.0,
                    "cuisines": ["Healthy", "Salad", "Continental"],
                    "additional_preferences": "vegetarian options, organic, low calorie, gluten-free"
                },
                expected_constraints={
                    "location_match": "Indiranagar",
                    "min_cost": 600,
                    "max_cost": 1800,
                    "min_rating": 4.0,
                    "cuisine_match": ["Healthy", "Salad", "Continental"]
                },
                description="Health-conscious user with dietary restrictions",
                tags=["health", "dietary", "vegetarian"]
            )
        ])
        
        # Constraint-heavy scenarios
        test_cases.extend([
            GoldenTestCase(
                name="tight_constraints",
                scenario=TestScenario.CONSTRAINT_HEAVY,
                preferences={
                    "location": "Koramangala",
                    "budget": {"min": 1000, "max": 1200},
                    "minimum_rating": 4.5,
                    "cuisines": ["Italian"],
                    "additional_preferences": "outdoor seating, accepts cards, lunch buffet"
                },
                expected_constraints={
                    "location_match": "Koramangala",
                    "min_cost": 1000,
                    "max_cost": 1200,
                    "min_rating": 4.5,
                    "cuisine_match": ["Italian"]
                },
                description="Very tight constraints across multiple dimensions",
                tags=["tight_constraints", "specific", "challenging"]
            )
        ])
        
        # Minimal preferences
        test_cases.extend([
            GoldenTestCase(
                name="minimal_input",
                scenario=TestScenario.MINIMAL_PREFERENCES,
                preferences={
                    "location": "Bellandur",
                    "budget": {"min": 0, "max": 2000},
                    "minimum_rating": 0,
                    "cuisines": [],
                    "additional_preferences": None
                },
                expected_constraints={
                    "location_match": "Bellandur",
                    "max_cost": 2000
                },
                description="User with minimal preferences, testing system defaults",
                tags=["minimal", "basic", "defaults"]
            )
        ])
        
        # Extreme values
        test_cases.extend([
            GoldenTestCase(
                name="zero_budget",
                scenario=TestScenario.EXTREME_VALUES,
                preferences={
                    "location": "Bellandur",
                    "budget": {"min": 0, "max": 0},
                    "minimum_rating": 3.0,
                    "cuisines": [],
                    "additional_preferences": "free or very cheap options"
                },
                expected_constraints={
                    "location_match": "Bellandur",
                    "max_cost": 0,
                    "min_rating": 3.0
                },
                description="Edge case with zero budget constraint",
                tags=["extreme", "zero_budget", "edge_case"]
            ),
            GoldenTestCase(
                name="perfect_rating",
                scenario=TestScenario.EXTREME_VALUES,
                preferences={
                    "location": "Indiranagar",
                    "budget": {"min": 0, "max": 5000},
                    "minimum_rating": 5.0,
                    "cuisines": [],
                    "additional_preferences": "perfect 5-star rating only"
                },
                expected_constraints={
                    "location_match": "Indiranagar",
                    "max_cost": 5000,
                    "min_rating": 5.0
                },
                description="Edge case requiring perfect 5.0 rating",
                tags=["extreme", "perfect_rating", "high_standards"]
            )
        ])
        
        return test_cases
    
    def get_test_cases_by_scenario(self, scenario: TestScenario) -> List[GoldenTestCase]:
        """Get all test cases for a specific scenario."""
        return [tc for tc in self.test_cases if tc.scenario == scenario]
    
    def get_test_cases_by_tag(self, tag: str) -> List[GoldenTestCase]:
        """Get all test cases with a specific tag."""
        return [tc for tc in self.test_cases if tag in tc.tags]
    
    def get_all_test_cases(self) -> List[GoldenTestCase]:
        """Get all test cases."""
        return self.test_cases
    
    def save_test_cases(self, file_path: str) -> None:
        """Save test cases to JSON file."""
        test_data = []
        for tc in self.test_cases:
            test_data.append({
                "name": tc.name,
                "scenario": tc.scenario.value,
                "preferences": tc.preferences,
                "expected_constraints": tc.expected_constraints,
                "description": tc.description,
                "tags": tc.tags
            })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    def load_test_cases(self, file_path: str) -> None:
        """Load test cases from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        self.test_cases = []
        for item in test_data:
            test_case = GoldenTestCase(
                name=item["name"],
                scenario=TestScenario(item["scenario"]),
                preferences=item["preferences"],
                expected_constraints=item["expected_constraints"],
                description=item["description"],
                tags=item["tags"]
            )
            self.test_cases.append(test_case)
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the test suite."""
        scenario_counts = {}
        tag_counts = {}
        
        for tc in self.test_cases:
            # Count scenarios
            scenario_name = tc.scenario.value
            scenario_counts[scenario_name] = scenario_counts.get(scenario_name, 0) + 1
            
            # Count tags
            for tag in tc.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            "total_test_cases": len(self.test_cases),
            "scenarios": scenario_counts,
            "tags": tag_counts,
            "scenario_types": list(TestScenario)
        }
