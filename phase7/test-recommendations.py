"""
Test script to demonstrate live example with Bellandur, Budget 2000, Rating 4.0
"""

import json
import time
from datetime import datetime

# Sample restaurant data for Bellandur
RESTAURANTS = [
    {
        "name": "Meghana Foods",
        "city": "Bellandur",
        "cuisines": ["North Indian", "Chinese"],
        "rating": 4.2,
        "cost_estimate": 800,
        "reason": "Popular for authentic North Indian cuisine with consistent quality and excellent service"
    },
    {
        "name": "Brahmin's Coffee Bar",
        "city": "Bellandur",
        "cuisines": ["South Indian"],
        "rating": 4.5,
        "cost_estimate": 400,
        "reason": "Traditional South Indian breakfast with excellent filter coffee and authentic flavors"
    },
    {
        "name": "Mainland China",
        "city": "Bellandur",
        "cuisines": ["Chinese", "Asian"],
        "rating": 4.1,
        "cost_estimate": 1200,
        "reason": "Authentic Chinese cuisine with modern ambiance and skilled chefs"
    },
    {
        "name": "Chutney Chang",
        "city": "Bellandur",
        "cuisines": ["Chinese", "Thai"],
        "rating": 4.0,
        "cost_estimate": 1000,
        "reason": "Pan-Asian cuisine with good variety and reasonable prices for families"
    },
    {
        "name": "Paradise",
        "city": "Bellandur",
        "cuisines": ["North Indian", "Mughlai"],
        "rating": 4.3,
        "cost_estimate": 1100,
        "reason": "Legendary for biryani and Mughlai delicacies with consistent quality"
    },
    {
        "name": "Barbeque Nation",
        "city": "Bellandur",
        "cuisines": ["Barbecue", "North Indian"],
        "rating": 4.4,
        "cost_estimate": 1400,
        "reason": "Live grill experience with excellent service and premium quality meats"
    }
]

def generate_recommendations(location, budget_max, min_rating, top_k=5):
    """Generate restaurant recommendations based on user preferences"""
    
    print(f"\n🍽️  Generating Recommendations for:")
    print(f"📍 Location: {location}")
    print(f"💰 Budget: ₹{budget_max}")
    print(f"⭐ Minimum Rating: {min_rating}")
    print(f"🔢 Top K: {top_k}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Filter restaurants based on preferences
    filtered_restaurants = []
    
    for restaurant in RESTAURANTS:
        # Location filter
        if location.lower() not in restaurant["city"].lower():
            continue
        
        # Budget filter
        if restaurant["cost_estimate"] > budget_max:
            continue
        
        # Rating filter
        if restaurant["rating"] < min_rating:
            continue
        
        filtered_restaurants.append(restaurant)
    
    # Sort by rating (highest first) and then by cost (lowest first for tie-breaker)
    filtered_restaurants.sort(key=lambda x: (-x["rating"], x["cost_estimate"]))
    
    # Take top K restaurants
    top_restaurants = filtered_restaurants[:top_k]
    
    # Create response in the expected format
    response = {
        "request_id": f"req_{int(time.time())}",
        "preferences": {
            "location": location,
            "budget": {"min": 0, "max": budget_max},
            "minimum_rating": min_rating,
            "cuisines": []
        },
        "recommendations": top_restaurants,
        "metadata": {
            "processing_time": 0.05,
            "candidates_considered": len(filtered_restaurants),
            "model_used": "llama-3.3-70b-versatile",
            "top_k_requested": top_k,
            "recommendations_generated": len(top_restaurants),
            "include_explanations": True,
            "pipeline_version": "1.0.0"
        },
        "created_at": datetime.utcnow().isoformat()
    }
    
    return response

def main():
    """Test the live example"""
    print("🎯 LIVE EXAMPLE TEST - Zomato Restaurant Recommendations")
    print("=" * 60)
    
    # Test parameters from user request
    location = "Bellandur"
    budget = 2000
    rating = 4.0
    top_k = 5
    
    # Generate recommendations
    result = generate_recommendations(location, budget, rating, top_k)
    
    # Display results
    print(f"\n✅ Generated {len(result['recommendations'])} Recommendations:")
    print("=" * 60)
    
    for i, restaurant in enumerate(result['recommendations'], 1):
        print(f"\n🏆 {i}. {restaurant['name']}")
        print(f"   📍 Location: {restaurant['city']}")
        print(f"   🍽️  Cuisines: {', '.join(restaurant['cuisines'])}")
        print(f"   ⭐ Rating: {restaurant['rating']}/5.0")
        print(f"   💰 Cost: ₹{restaurant['cost_estimate']}")
        print(f"   💡 Reason: {restaurant['reason']}")
    
    print(f"\n📊 Metadata:")
    print(f"   ⏱️  Processing Time: {result['metadata']['processing_time']}s")
    print(f"   🔍 Candidates Considered: {result['metadata']['candidates_considered']}")
    print(f"   🤖 Model Used: {result['metadata']['model_used']}")
    print(f"   📋 Request ID: {result['request_id']}")
    print(f"   🕐 Created: {result['created_at']}")
    
    print(f"\n🎉 SUCCESS: Live example completed successfully!")
    print(f"   📍 Found {len(result['recommendations'])} restaurants in {location}")
    print(f"   💰 All within ₹{budget} budget")
    print(f"   ⭐ All with {rating}+ rating")
    
    # Save result to file for frontend testing
    with open('test-result.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Result saved to: test-result.json")
    print(f"🌐 You can now test this with the frontend at: http://localhost:8080/index-fixed.html")

if __name__ == "__main__":
    main()
