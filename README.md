# Message Post App

## Overview
The **Message Post App** is a web application that allows users to create, retrieve, update, and comment on posts. It is built using **Flask** as the backend framework and **Google Cloud Firestore** as the database. The application is designed to be deployed on **Google Cloud App Engine**.

## Features
- **Create Posts**: Users can submit posts with a subject and body.
- **Retrieve Posts**: Fetch all posts or a specific post by ID.
- **Update Posts**: Modify the subject and body of an existing post.
- **Add Comments**: Append comments to a post, stored in an embedded array.
- **Firestore Integration**: Uses Firestore for structured and scalable data storage.
- **Unit Testing**: Includes test cases for API endpoints and Firestore queries.

## Architecture
The application follows a **server-client model** where the backend serves API endpoints for post management. The key components include:

- **Flask API Server** (`message_post_server.py`)
- **Firestore Database** (`firestore_queries.py`)
- **Unit Tests** (`test_flask_apis.py`, `test_firestore_queries.py`)
- **Deployment Configuration** (`app.yaml`, `requirements.txt`)

## API Endpoints
### 📝 Posts
| Method | Endpoint           | Description                   |
|--------|--------------------|-------------------------------|
| POST   | `/posts`           | Create a new post             |
| GET    | `/posts`           | Retrieve all posts            |
| GET    | `/posts/<post_id>` | Retrieve a specific post      |
| PUT    | `/posts/<post_id>` | Update an existing post       |

### 💬 Comments
| Method | Endpoint                         | Description                   |
|--------|----------------------------------|-------------------------------|
| POST   | `/posts/<post_id>/comments`      | Add a comment to a post       |

## Database Structure
Each post is stored as a **document** in Firestore under the `collection_posts` collection.

### Example Post Document:
```json
{
  "author": "user@example.com",
  "creation_date": "2025-03-17T10:00:00Z",
  "change_date": "2025-03-17T10:30:00Z",
  "subject": "My First Post",
  "body": "This is the content of my post.",
  "comments": [
    {
      "author": "commenter@example.com",
      "creation_date": "2025-03-17T11:00:00Z",
      "change_date": "2025-03-17T11:10:00Z",
      "body": "Nice post!"
    }
  ]
}
