#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '.')

def test_new_review_structure():
    print("🧪 Testing New Review Structure (Rating + Text)...")
    
    try:
        from main import write_review, get_review, list_reviews
        
        # Test 1: Write a review with rating and text
        print("\n1. Testing write_review with rating and text:")
        result1 = write_review("Test Movie 2024", 8, "Amazing cinematography and great story!")
        print(f"   Result: {result1}")
        
        # Test 2: Write another review
        print("\n2. Testing second review:")
        result2 = write_review("Inception", 9, "Mind-bending masterpiece!")
        print(f"   Result: {result2}")
        
        # Test 3: Get a specific review
        print("\n3. Testing get_review:")
        get_result = get_review("Test Movie 2024")
        print(f"   Result: {get_result}")
        
        # Test 4: List all reviews
        print("\n4. Testing list_reviews:")
        list_result = list_reviews()
        print(f"   Result: {list_result}")
        
        # Test 5: Check the actual JSON file
        print("\n5. Checking actual JSON file content:")
        import json
        try:
            with open("/Users/jeyashreekrishan/workspace/imdb-mcp-server/my_reviews.json", "r") as f:
                file_content = json.load(f)
            print(f"   JSON Content: {json.dumps(file_content, indent=2)}")
        except FileNotFoundError:
            print("   JSON file not found")
        except Exception as e:
            print(f"   Error reading JSON: {e}")
            
        print("\n✅ Test complete!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_new_review_structure() 