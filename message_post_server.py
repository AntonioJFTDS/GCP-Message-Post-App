from flask import Flask, request, jsonify
from google.cloud import firestore
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"


db = firestore.Client(database="antoniodb")
COLLECTION_NAME = "collection_posts"

# ✅ Create a Post (POST /posts)
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    if not data or "subject" not in data or "body" not in data:
        return jsonify({"error": "Missing subject or body"}), 400

    new_post = {
        "author": "test_user@gmail.com",  # Dummy user, replace if authentication is added
        "creation_date": datetime.datetime.utcnow().isoformat(),
        "change_date": datetime.datetime.utcnow().isoformat(),
        "subject": data["subject"],
        "body": data["body"],
        "comments": []  # Start with an empty list of comments
    }
    
    doc_ref = db.collection(COLLECTION_NAME).add(new_post)
    new_post["id"] = doc_ref[1].id
    return jsonify(new_post), 201

# ✅ Get All Posts (GET /posts)
@app.route("/posts", methods=["GET"])
def get_posts():
    posts_ref = db.collection(COLLECTION_NAME).stream()
    posts = [{"id": doc.id, **doc.to_dict()} for doc in posts_ref]
    return jsonify(posts), 200

# ✅ Get a Specific Post (GET /posts/<post_id>)
@app.route("/posts/<post_id>", methods=["GET"])
def get_post(post_id):
    post_ref = db.collection(COLLECTION_NAME).document(post_id).get()
    if post_ref.exists:
        return jsonify({"id": post_id, **post_ref.to_dict()}), 200
    return jsonify({"error": "Post not found"}), 404

# ✅ Update a Post (PUT /posts/<post_id>)
@app.route("/posts/<post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json()
    if not data or "subject" not in data or "body" not in data:
        return jsonify({"error": "Missing subject or body"}), 400

    post_ref = db.collection(COLLECTION_NAME).document(post_id)
    post = post_ref.get()
    if not post.exists:
        return jsonify({"error": "Post not found"}), 404

    updated_data = {
        "subject": data["subject"],
        "body": data["body"],
        "change_date": datetime.datetime.utcnow().isoformat()
    }
    post_ref.update(updated_data)
    return jsonify({"id": post_id, **updated_data}), 200

# ✅ Add a Comment to a Post (POST /posts/<post_id>/comments)
@app.route("/posts/<post_id>/comments", methods=["POST"])
def add_comment(post_id):
    data = request.get_json()
    if not data or "body" not in data:
        return jsonify({"error": "Missing comment body"}), 400

    post_ref = db.collection(COLLECTION_NAME).document(post_id)
    post = post_ref.get()
    if not post.exists:
        return jsonify({"error": "Post not found"}), 404

    comment = {
        "author": "comment_user@gmail.com",  # Dummy user
        "creation_date": datetime.datetime.utcnow().isoformat(),
        "change_date": datetime.datetime.utcnow().isoformat(),
        "body": data["body"]
    }
    post_ref.update({"comments": firestore.ArrayUnion([comment])})
    return jsonify({"message": "Comment added", "comment": comment}), 201

# ✅ Run Flask Server
if __name__ == "__main__":
    app.run(debug=True)
