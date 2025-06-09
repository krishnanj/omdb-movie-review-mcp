import json
import os

REVIEW_FILE = "my_reviews.json"

def write_review(title: str, review: str) -> dict:
    """Write or update a personal review for a movie"""
    reviews = {}
    if os.path.exists(REVIEW_FILE):
        with open(REVIEW_FILE, "r") as f:
            reviews = json.load(f)
    reviews[title] = review
    with open(REVIEW_FILE, "w") as f:
        json.dump(reviews, f, indent=2)
    return {"message": "Review saved", "movie": title}

def get_review(title: str) -> dict:
    """Get your personal review for a movie"""
    if not os.path.exists(REVIEW_FILE):
        return {"error": "No reviews found"}
    with open(REVIEW_FILE, "r") as f:
        reviews = json.load(f)
    return {"review": reviews.get(title, "No review found")}

def list_reviews() -> list:
    """List all reviewed movie titles"""
    if not os.path.exists(REVIEW_FILE):
        return []
    with open(REVIEW_FILE, "r") as f:
        reviews = json.load(f)
    return list(reviews.keys())

def delete_review(title: str) -> dict:
    """Delete a review for a movie"""
    if not os.path.exists(REVIEW_FILE):
        return {"error": "No reviews found"}
    with open(REVIEW_FILE, "r") as f:
        reviews = json.load(f)
    if title in reviews:
        del reviews[title]
        with open(REVIEW_FILE, "w") as f:
            json.dump(reviews, f, indent=2)
        return {"message": f"Deleted review for {title}"}
    return {"error": f"No review found for {title}"}