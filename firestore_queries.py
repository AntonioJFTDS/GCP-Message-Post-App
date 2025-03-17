from google.cloud import firestore
import datetime

# Initialize Firestore client
db = firestore.Client(database="antoniodb")
COLLECTION_NAME = "collection_posts"

# ✅ Helper function to check if a post exists before performing any operation
# This function prevents actions on non-existent posts
def post_exists(post_id):
    post_ref = db.collection(COLLECTION_NAME).document(post_id).get()
    return post_ref.exists

# ✅ Insert a new post
def insert_post(author, subject, body):
    if not author or not subject or not body:
        raise ValueError("Author, subject, and body are required.")
    
    post_data = {
        "author": author,
        "creation_date": datetime.datetime.utcnow().isoformat(),
        "change_date": datetime.datetime.utcnow().isoformat(),
        "subject": subject,
        "body": body,
        "comments": []  # Empty comments list
    }
    doc_ref = db.collection(COLLECTION_NAME).add(post_data)
    print(f"Post created with ID: {doc_ref[1].id}")
    return doc_ref[1].id

# ✅ Retrieve all posts
def get_all_posts():
    posts = db.collection(COLLECTION_NAME).stream()
    return [{"id": post.id, **post.to_dict()} for post in posts]

# ✅ Retrieve a specific post by ID
def get_post(post_id):
    if not post_id or not post_exists(post_id):
        raise ValueError("Post not found.")
    
    post_ref = db.collection(COLLECTION_NAME).document(post_id).get()
    return {"id": post_id, **post_ref.to_dict()}

# ✅ Update a post
def update_post(post_id, subject, body):
    if not post_id or not subject or not body:
        raise ValueError("Post ID, subject, and body are required.")
    
    if not post_exists(post_id):
        raise ValueError("Post not found.")
    
    post_ref = db.collection(COLLECTION_NAME).document(post_id)
    post_ref.update({
        "subject": subject,
        "body": body,
        "change_date": datetime.datetime.utcnow().isoformat()
    })
    print("Post updated successfully.")

# ✅ Add a comment to a post
def add_comment(post_id, author, body):
    if not post_id or not author or not body:
        raise ValueError("Post ID, author, and body are required.")
    
    if not post_exists(post_id):
        raise ValueError("Post not found.")
    
    post_ref = db.collection(COLLECTION_NAME).document(post_id)
    comment = {
        "author": author,
        "creation_date": datetime.datetime.utcnow().isoformat(),
        "change_date": datetime.datetime.utcnow().isoformat(),
        "body": body
    }
    post_ref.update({"comments": firestore.ArrayUnion([comment])})
    print("Comment added successfully.")

# ✅ Update a comment
def update_comment(post_id, creation_date, new_body):
    if not post_id or not creation_date or not new_body:
        raise ValueError("Post ID, comment creation date, and new body are required.")
    
    if not post_exists(post_id):
        raise ValueError("Post not found.")
    
    post_ref = db.collection(COLLECTION_NAME).document(post_id)
    post = post_ref.get()
    comments = post.to_dict().get("comments", [])
    updated_comments = []
    comment_found = False

    for comment in comments:
        if comment["creation_date"] == creation_date:
            comment["body"] = new_body
            comment["change_date"] = datetime.datetime.utcnow().isoformat()
            comment_found = True
        updated_comments.append(comment)
    
    if comment_found:
        post_ref.update({"comments": updated_comments})
        print("Comment updated successfully.")
    else:
        raise ValueError("Comment not found.")

# Example usage
if __name__ == "__main__":
    post_id = insert_post("user123@gmail.com", "Test Post", "This is a test post.")
    get_all_posts()
    get_post(post_id)
    update_post(post_id, "Updated Post", "Updated body text.")
    add_comment(post_id, "commenter1@gmail.com", "Nice post!")
    update_comment(post_id, "2025-03-13T11:30:00Z", "Updated comment!")
