#!/usr/bin/env python3
"""
Quick test script to verify the new microservices are working
Run this AFTER docker-compose is up and running
"""

import requests
import json
import time

API_BASE = "http://localhost:5001/api"

def test_health():
    """Test API health"""
    print("Testing API health...")
    response = requests.get(f"{API_BASE}/health")
    if response.status_code == 200:
        print("✓ API is healthy")
        return True
    else:
        print("✗ API health check failed")
        return False

def test_create_post():
    """Create a test post and check sentiment analysis"""
    print("\nCreating test post with sentiment...")
    
    # Create a positive post
    positive_post = {
        "user": "test_user",
        "text": "This is absolutely wonderful and amazing! I love this product so much!"
    }
    
    response = requests.post(
        f"{API_BASE}/posts",
        json=positive_post,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 201:
        print(f"✗ Failed to create post: {response.text}")
        return None
    
    post = response.json()['post']
    post_id = post['id']
    print(f"✓ Created post ID: {post_id}")
    
    # Wait for sentiment analysis (async processing)
    print("Waiting 5 seconds for sentiment analysis...")
    time.sleep(5)
    
    # Get post with sentiment
    response = requests.get(f"{API_BASE}/posts/{post_id}")
    if response.status_code == 200:
        post_data = response.json()
        sentiment_label = post_data.get('sentiment_label')
        sentiment_score = post_data.get('sentiment_score')
        
        if sentiment_label:
            print(f"✓ Sentiment Analysis Complete:")
            print(f"  Label: {sentiment_label}")
            print(f"  Score: {sentiment_score}")
            return post_id
        else:
            print("⚠ Sentiment not yet processed (may need more time)")
            return post_id
    else:
        print("✗ Failed to retrieve post")
        return None

def test_get_all_posts():
    """Get all posts and check sentiment data"""
    print("\nFetching all posts...")
    response = requests.get(f"{API_BASE}/posts")
    
    if response.status_code == 200:
        data = response.json()
        posts = data['posts']
        print(f"✓ Retrieved {len(posts)} posts")
        
        # Check if any have sentiment
        with_sentiment = sum(1 for p in posts if p.get('sentiment_label'))
        print(f"  Posts with sentiment: {with_sentiment}/{len(posts)}")
        
        return True
    else:
        print("✗ Failed to retrieve posts")
        return False

def test_text_generation():
    """Test text generation endpoint"""
    print("\nTesting text generation...")
    
    response = requests.post(
        f"{API_BASE}/posts/generate",
        json={"prompt": "Once upon a time", "max_length": 50},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Text generation endpoint working")
        print(f"  Response: {data.get('message')}")
        return True
    else:
        print(f"✗ Text generation failed: {response.text}")
        return False

def main():
    print("="*60)
    print("TESTING NEW MICROSERVICES")
    print("="*60)
    print("\nMake sure docker-compose is running first!")
    print("Run: docker-compose up -d\n")
    
    try:
        # Test 1: Health check
        if not test_health():
            print("\n✗ API not available. Is docker-compose running?")
            return
        
        # Test 2: Create post and check sentiment
        test_create_post()
        
        # Test 3: Get all posts
        test_get_all_posts()
        
        # Test 4: Text generation
        test_text_generation()
        
        print("\n" + "="*60)
        print("TESTING COMPLETE!")
        print("="*60)
        print("\nCheck the logs to see microservices working:")
        print("  docker-compose logs sentiment-analyzer")
        print("  docker-compose logs text-generator")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Cannot connect to API. Is docker-compose running?")
        print("Run: docker-compose up -d")
    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    main()
