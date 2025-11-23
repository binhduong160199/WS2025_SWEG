# REST API Quick Reference

## Base URL
```
http://localhost:5000/api
```

---

## Endpoints

### 1. Health Check
```http
GET /health
```
**Response:** `200 OK`
```json
{
  "status": "healthy",
  "message": "Social Media API is running"
}
```

---

### 2. Create Post
```http
POST /posts
Content-Type: application/json
```
**Request Body:**
```json
{
  "user": "john_doe",
  "text": "Hello World!",
  "image": "base64_encoded_image_data"  // optional
}
```
**Response:** `201 Created`
```json
{
  "message": "Post created successfully",
  "post": {
    "id": 1,
    "user": "john_doe",
    "text": "Hello World!",
    "image": null,
    "created_at": "2025-11-23 10:30:45"
  }
}
```

---

### 3. Get All Posts
```http
GET /posts?limit=10
```
**Query Parameters:**
- `limit` (optional): Maximum number of posts

**Response:** `200 OK`
```json
{
  "count": 3,
  "posts": [
    {
      "id": 3,
      "user": "charlie",
      "text": "Another post",
      "created_at": "2025-11-23 10:32:00",
      "has_image": false
    }
  ]
}
```

---

### 4. Get Post by ID
```http
GET /posts/{post_id}
```
**Response:** `200 OK`
```json
{
  "id": 1,
  "user": "john_doe",
  "text": "Hello World!",
  "image": null,
  "created_at": "2025-11-23 10:30:45"
}
```

---

### 5. Get Latest Post
```http
GET /posts/latest
```
**Response:** `200 OK`
```json
{
  "id": 10,
  "user": "latest_user",
  "text": "This is the latest post",
  "image": null,
  "created_at": "2025-11-23 11:00:00"
}
```

---

### 6. Search Posts
```http
GET /posts/search?q=coffee
```
**Query Parameters:**
- `q` (required): Search query string

**Response:** `200 OK`
```json
{
  "query": "coffee",
  "count": 2,
  "posts": [
    {
      "id": 2,
      "user": "bob",
      "text": "Coffee is great!",
      "created_at": "2025-11-23 10:31:00",
      "has_image": false
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "User field is required and cannot be empty"
}
```

### 404 Not Found
```json
{
  "error": "Post not found"
}
```

### 405 Method Not Allowed
```json
{
  "error": "Method not allowed"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error: details"
}
```

---

## Testing

### Run all tests:
```bash
python -m pytest tests/ -v
```

### Run specific test file:
```bash
python -m pytest tests/test_api.py -v
```

### Run with coverage:
```bash
python -m pytest tests/ --cov=app --cov-report=html
```

---

## cURL Examples

### Create a post:
```bash
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"user": "alice", "text": "My first post!"}'
```

### Get all posts:
```bash
curl http://localhost:5000/api/posts
```

### Get specific post:
```bash
curl http://localhost:5000/api/posts/1
```

### Search posts:
```bash
curl "http://localhost:5000/api/posts/search?q=hello"
```

### Get latest post:
```bash
curl http://localhost:5000/api/posts/latest
```

---

## Python Example

```python
import requests

# Create a post
response = requests.post('http://localhost:5000/api/posts', json={
    'user': 'john_doe',
    'text': 'Hello from Python!'
})
print(response.json())

# Get all posts
response = requests.get('http://localhost:5000/api/posts')
posts = response.json()
print(f"Found {posts['count']} posts")

# Search posts
response = requests.get('http://localhost:5000/api/posts/search', params={'q': 'hello'})
results = response.json()
print(f"Search returned {results['count']} results")
```

---

## Data Validation Rules

- **User**: Required, 1-50 characters
- **Text**: Required, 1-500 characters
- **Image**: Optional, valid base64 string
- **Search Query**: Required, minimum 1 character

---

For complete API documentation, see: `docs/openapi.yaml`
