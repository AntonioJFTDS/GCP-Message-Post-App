# Message Post App - Project Description

## Overview
The **Message Post App** is a web application that allows users to create, retrieve, update, and comment on posts. It is built using **Flask** for the backend and **Google Cloud Firestore** for the database. The app is deployed on **Google Cloud App Engine**.

## Features
- Create new posts with a subject and body.
- Retrieve all posts or a specific post by ID.
- Update existing posts.
- Add comments to posts.
- Store data in **Firestore** under the `collection_posts` collection.

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** Google Cloud Firestore
- **Hosting:** Google Cloud App Engine
- **Web Server:** Gunicorn
- **Testing:** unittest

## Firestore Structure
Each post is stored as a document inside `collection_posts`. Each post can have multiple comments, stored as an array inside the document.

### Example Post Document:
```json
{
  "author": "user@example.com",
  "creation_date": "2025-03-13T10:00:00Z",
  "change_date": "2025-03-13T11:00:00Z",
  "subject": "My First Post",
  "body": "This is the content of my post.",
  "comments": [
    {
      "author": "commenter1@example.com",
      "creation_date": "2025-03-13T11:30:00Z",
      "change_date": "2025-03-13T11:45:00Z",
      "body": "Nice post!"
    }
  ]
}
```

## API Endpoints
### 1. Create a Post
- **Endpoint:** `POST /posts`
- **Request Body:**
  ```json
  {
    "subject": "New Post",
    "body": "This is a new post"
  }
  ```
- **Response:** Returns the created post with an auto-generated ID.

### 2. Get All Posts
- **Endpoint:** `GET /posts`
- **Response:** Returns a list of all posts.

### 3. Get a Specific Post
- **Endpoint:** `GET /posts/{post_id}`
- **Response:** Returns the post with the specified ID.

### 4. Update a Post
- **Endpoint:** `PUT /posts/{post_id}`
- **Request Body:**
  ```json
  {
    "subject": "Updated Title",
    "body": "Updated post content"
  }
  ```
- **Response:** Updates the specified post.

### 5. Add a Comment
- **Endpoint:** `POST /posts/{post_id}/comments`
- **Request Body:**
  ```json
  {
    "body": "This is a comment"
  }
  ```
- **Response:** Adds a comment to the specified post.

## Deployment on Google Cloud
### Prerequisites
- Google Cloud SDK installed
- A Google Cloud project with App Engine enabled

### Steps
1. Authenticate with Google Cloud:
   ```sh
   gcloud auth login
   ```
2. Set the active project:
   ```sh
   gcloud config set project YOUR_PROJECT_ID
   ```
3. Deploy the application:
   ```sh
   gcloud app deploy
   ```
4. Access the deployed app:
   ```sh
   gcloud app browse
   ```

## Testing
Unit tests are available in:
- `test_flask_apis.py` (local API testing)
- `test_deployed_flask_apis.py` (testing deployed APIs)
- `test_firestore_queries.py` (testing Firestore queries)

Run tests with:
```sh
python -m unittest discover
```

## Dependencies
The required packages are listed in `requirements.txt`:
```txt
flask
google-cloud-firestore
gunicorn
```

## Conclusion
This app demonstrates how to integrate a Flask backend with Firestore and deploy it to Google Cloud. It is structured for easy API interaction and scalable data management.

