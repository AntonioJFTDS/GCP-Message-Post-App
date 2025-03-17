# Message Post App - Project Documentation

## **1️⃣ Database Name: `antoniodb`**

- This project uses Firestore as the database.
- The Firestore database being used is explicitly named **`antoniodb`**, rather than the default database.
- Firestore automatically **creates collections** when the first document is inserted.

## **2️⃣ Collection Name: `collection_posts`**

- This collection **stores all user posts** and their **comments** in a structured way.
- Firestore automatically **creates this collection** when the first document is inserted.

---

## **3️⃣ Document Structure (Posts & Comments)**

Each **post** is stored as a **document** inside `collection_posts`.A **post can have multiple comments**, stored as an **array inside the post document**.

### **📝 Example Post with Multiple Comments**

```json
{
  "author": "user123@gmail.com",
  "creation_date": "2025-03-13T10:00:00Z",
  "change_date": "2025-03-13T11:00:00Z",
  "subject": "My First Post",
  "body": "This is the content of my post.",
  "comments": [
    {
      "author": "commenter1@gmail.com",
      "creation_date": "2025-03-13T11:30:00Z",
      "change_date": "2025-03-13T11:45:00Z",
      "body": "Nice post!"
    },
    {
      "author": "commenter2@gmail.com",
      "creation_date": "2025-03-13T12:00:00Z",
      "change_date": "2025-03-13T12:10:00Z",
      "body": "Thanks for sharing!"
    }
  ]
}
```

---

## **4️⃣ Why This Structure?**

### **✅ Supports Multiple Comments Per Post**

- Each **post can have multiple comments**, stored inside the **comments array**.
- This structure allows **fast access** to all comments when fetching a post.

### **✅ Optimized for Reads**

- Firestore does **not support SQL-style JOINs**, so **embedding comments** inside the post **reduces queries**.
- **Fetching a post automatically includes its comments**, reducing API calls.

### **✅ Simplifies Updates**

- The `change_date` field ensures that **both posts and comments track updates**.
- If a comment is modified, its `change_date` is updated.

---

## **5️⃣ Alternative Approach (Separate `comments` Collection)**

For **very high comment volume** (e.g., thousands per post), an alternative structure would be:

- **`collection_posts` → Stores posts (without comments)**
- **`collection_comments` → Stores each comment separately with a reference to `post_id`**

### **🚫 Why Not Use This Now?**

| **Option**                        | **Pros**                           | **Cons**                                   |
| --------------------------------- | ---------------------------------- | ------------------------------------------ |
| ✅ Embedded Comments (Current)     | Fewer queries, faster reads        | Slower for posts with **10,000+ comments** |
| 🚫 Separate `comments` Collection | Scales better for massive comments | Requires **multiple Firestore reads**      |

For this project, **embedding comments inside posts is the best approach**.

---

## **📌 Summary**

### **Post Fields**

| **Field**       | **Purpose**                              |
| --------------- | ---------------------------------------- |
| `author`        | Stores the email of the post creator     |
| `creation_date` | Timestamp when the post was created      |
| `change_date`   | Timestamp when the post was last updated |
| `subject`       | Title of the post                        |
| `body`          | Content of the post                      |
| `comments`      | List of embedded comments                |

### **Comment Fields**

| **Field**       | **Purpose**                              |
| --------------- | ---------------------------------------- |
| `author`        | Stores the email of the comment creator  |
| `creation_date` | Timestamp when the comment was created   |
| `change_date`   | Timestamp when the comment was last updated |
| `body`          | Content of the comment                   |

---

## **6️⃣ Firestore Query Tests**

This section explains how the `test_firestore_queries.py` file validates Firestore operations to ensure the database functions correctly.

### **✅ Purpose of the Test File**
The `test_firestore_queries.py` file is designed to verify the correctness of Firestore operations in `firestore_queries.py`. It ensures that:
- Posts can be created, retrieved, and updated correctly.
- Comments can be added and updated inside posts.
- Non-existent posts and comments return appropriate errors.

### **✅ What Does This Test?**

#### **1️⃣ Create a Post**
- Ensures that a post is successfully created in Firestore.
- Validates that the created post has the expected fields.

#### **2️⃣ Retrieve All Posts**
- Ensures that posts can be retrieved from Firestore.

#### **3️⃣ Retrieve a Specific Post by ID**
- Confirms that retrieving a post by its ID works as expected.
- Validates the subject and body of the retrieved post.

#### **4️⃣ Update a Post**
- Updates an existing post and checks if the changes are saved.

#### **5️⃣ Add a Comment to a Post**
- Ensures a comment can be added to an existing post.
- Validates that the comment appears in the post.

#### **6️⃣ Update a Comment**
- Modifies a comment and checks if the changes are applied.

#### **7️⃣ Handle Invalid Post IDs**
- Tests querying a non-existent post and expects an error.

#### **8️⃣ Update a Non-Existent Post**
- Ensures updating an invalid post ID raises an error.

#### **9️⃣ Add a Comment to a Non-Existent Post**
- Ensures trying to add a comment to a non-existent post raises an error.

#### **🔟 Update a Non-Existent Comment**
- Ensures trying to update a non-existent comment returns an error.

### **How to Run the Tests**
To execute the test file, run the following command:
```sh
python -m unittest test_firestore_queries.py
```

### **Expected Output (Success Case)**
```
.....
----------------------------------------------------------------------
Ran 10 tests in X.XXXs

OK
Test data cleaned up.
```
If an error occurs, the test will indicate the failure and provide debugging details.


## **7️⃣ `message_post_server.py` Explanation**

This file contains the **Flask server** that handles the API endpoints for managing posts and comments. It uses **Google Cloud Firestore** as the database.

### **Dependencies**

-   `Flask`: A micro web framework for building the API.
-   `google-cloud-firestore`: The Firestore client library for Python.
-   `datetime`:  For handling timestamps.

### **Initialization**

-   `app = Flask(__name__)`: Initializes the Flask application.
-   `db = firestore.Client(database="antoniodb")`: Initializes the Firestore client, connecting to your antoniodb Firestore database.
-   `COLLECTION_NAME = "collection_posts"`:  Defines the name of the Firestore collection used to store posts.

### **Routes and Functions**

1.  **Home Route (`/`)**

    -   `@app.route('/')`
    -   Defines the route for the root URL.
    -   `def home():`
        -   Returns a simple "Hello World!" message.
        -   This is a basic check to ensure the server is running.

2.  **Create a Post (`POST /posts`)**

    -   `@app.route("/posts", methods=["POST"])`
    -   Defines the route for creating a new post. It only accepts POST requests.
    -   `def create_post():`
        -   `data = request.get_json()`: Retrieves the JSON data from the request body.
        -   **Validation:**
            -   Checks if the `subject` and `body` are present in the data. If not, it returns an error response (400 Bad Request).
        -   `new_post`:
            -   Creates a dictionary `new_post` containing the post data:
                -   `author`:  Currently a dummy user.  **Important:** This should be replaced with actual user authentication in a production environment.
                -   `creation_date`:  The current UTC timestamp in ISO format.
                -   `change_date`:  The current UTC timestamp in ISO format.
                -   `subject`:  The subject of the post from the request.
                -   `body`:  The body of the post from the request.
                -   `comments`: Initializes an empty list to store comments.
        -   `doc_ref = db.collection(COLLECTION_NAME).add(new_post)`:
            -   Adds the `new_post` dictionary as a new document to the `collection_posts` collection in Firestore.
            -   `doc_ref` contains information about the newly created document.
        -   `new_post["id"] = doc_ref[1].id`:
            -   Adds the Firestore-generated document ID to the `new_post` dictionary for easier access.
        -   Returns the `new_post` dictionary as a JSON response with a 201 Created status code.

3.  **Get All Posts (`GET /posts`)**

    -   `@app.route("/posts", methods=["GET"])`
    -   Defines the route for retrieving all posts. It only accepts GET requests.
    -   `def get_posts():`
        -   `posts_ref = db.collection(COLLECTION_NAME).stream()`:
            -   Retrieves a stream of all documents in the `collection_posts` collection. A stream allows you to efficiently iterate over the documents.
        -   `posts = [{"id": doc.id, **doc.to_dict()} for doc in posts_ref]`:
            -   Uses a list comprehension to build a list of post dictionaries.
            -   For each document (`doc`) in the stream:
                -   `doc.id`:  Retrieves the document's ID.
                -   `doc.to_dict()`:  Converts the document data to a Python dictionary.
                -   A new dictionary is created with `"id"` and all the fields from the document.
        -   Returns the list of `posts` as a JSON response with a 200 OK status code.

4.  **Get a Specific Post (`GET /posts/<post_id>`)**

    -   `@app.route("/posts/<post_id>", methods=["GET"])`
    -   Defines the route for retrieving a specific post by its ID.
    -   `def get_post(post_id):`
        -   `post_ref = db.collection(COLLECTION_NAME).document(post_id).get()`:
            -   Retrieves the document with the specified `post_id` from the `collection_posts` collection.
            -   `.get()` fetches the document.
        -   **Error Handling:**
            -   `if post_ref.exists:`: Checks if the document exists.
                -   If it exists, it returns a dictionary containing the post's "id" and its data (from `post_ref.to_dict()`) as a JSON response with a 200 OK status code.
            -   `else`: If the document does not exist, it returns an error message as a JSON response with a 404 Not Found status code.

5.  **Update a Post (`PUT /posts/<post_id>`)**

    -   `@app.route("/posts/<post_id>", methods=["PUT"])`
    -   Defines the route for updating an existing post.  It uses the PUT method, which is typically used for complete updates.
    -   `def update_post(post_id):`
        -   `data = request.get_json()`: Retrieves the JSON data from the request body, which should contain the updated post information.
        -   **Validation:**
            -   Checks if the `subject` and `body` are present in the data. If not, it returns an error response (400 Bad Request).
        -   `post_ref = db.collection(COLLECTION_NAME).document(post_id)`:
            -   Gets a reference to the document with the specified `post_id`.
        -   `post = post_ref.get()`:
            -   Fetches the current post document.
        -   **Error Handling:**
            -   `if not post.exists:`:  Checks if the post exists. If not, it returns an error message as a JSON response with a 404 Not Found status code.
        -   `updated_data`:
            -   Creates a dictionary `updated_data` containing the fields to be updated:
                -   `subject`:  The updated subject from the request.
                -   `body`:  The updated body from the request.
                -   `change_date`:  The current UTC timestamp in ISO format to reflect the update.
        -   `post_ref.update(updated_data)`:
            -   Updates the document in Firestore with the `updated_data`.  The `update()` method only modifies the specified fields, leaving other fields unchanged.
        -   Returns a JSON response with the `id` of the updated post and the `updated_data` with a 200 OK status code.

6.  **Add a Comment to a Post (`POST /posts/<post_id>/comments`)**

    -   `@app.route("/posts/<post_id>/comments", methods=["POST"])`
    -   Defines the route for adding a new comment to an existing post.
    -   `def add_comment(post_id):`
        -   `data = request.get_json()`:  Retrieves the JSON data from the request body, which should contain the comment data.
        -   **Validation:**
            -   Checks if the `body` of the comment is present in the data. If not, it returns an error response (400 Bad Request).
        -   `post_ref = db.collection(COLLECTION_NAME).document(post_id)`:
            -   Gets a reference to the document representing the post.
        -   `post = post_ref.get()`:
            -   Fetches the current post document.
        -   **Error Handling:**
            -   `if not post.exists:`: Checks if the post exists. If not, it returns an error message as a JSON response with a 404 Not Found status code.
        -   `comment`:
            -   Creates a dictionary `comment` representing the new comment:
                -   `author`: Currently a dummy user.  **Important:** This should be replaced with actual user authentication.
                -   `creation_date`:  The current UTC timestamp in ISO format.
                -   `change_date`:  The current UTC timestamp in ISO format.
                -   `body`:  The body of the comment from the request.
        -   `post_ref.update({"comments": firestore.ArrayUnion([comment])})`:
            -   Updates the post document by using `firestore.ArrayUnion([comment])` to add the new `comment` dictionary to the `comments` array within the post document. `ArrayUnion` ensures that the comment is added to the array without duplicating existing comments.
        -   Returns a JSON response with a success message and the newly added `comment` with a 201 Created status code.

7.  **Run the Flask Server**

    -   `if __name__ == "__main__":`
        -   This block ensures that the Flask development server is started only when the script is executed directly (not when imported as a module).
    -   `app.run(debug=True)`:
        -   Starts the Flask development server.
        -   `debug=True`:  Enables debug mode, which provides helpful error messages and automatic reloading when you make changes to the code.  **Important:** Do not use `debug=True` in a production environment.

### **Important Considerations**

-   **Authentication:** The code uses dummy users (`test_user@gmail.com`, `comment_user@gmail.com`).  In a real application, you **must** implement proper user authentication and authorization to secure your API.  This could involve using Firebase Authentication or another authentication provider.
-   **Error Handling:** The code includes basic error handling (e.g., checking for missing data, handling "post not found"). You should expand this to handle other potential errors and exceptions gracefully. Consider using more specific status codes and informative error messages.
-   **Validation and Sanitization:** The code performs minimal input validation.  You should add more robust validation and sanitization to prevent security vulnerabilities (e.g., injection attacks) and ensure data integrity.  Validate data types, lengths, and formats.
-   **Production Deployment:** The Flask development server (`app.run(debug=True)`) is **not suitable for production**. You will need to use a production-ready WSGI server (e.g., Gunicorn, uWSGI) and deploy your application to a suitable platform (e.g., Google Cloud Platform, AWS, Heroku).
-   **Security:** In addition to authentication, consider other security best practices, such as using HTTPS, protecting against Cross-Site Scripting (XSS), and preventing Cross-Site Request Forgery (CSRF).
-   **Testing:** The provided documentation includes a section on Firestore query tests. You should write comprehensive unit tests and integration tests to ensure that your API endpoints function correctly and that your Firestore interactions are working as expected.


---

## **8️⃣ `test_flask_apis.py` Explanation**

This file contains **unit tests** for the Flask API endpoints defined in `message_post_server.py`. It uses the `unittest` framework to verify that the API endpoints are functioning as expected.

### **Dependencies**

-   `unittest`: The Python unit testing framework.
-   `json`:  For handling JSON data in requests and responses.
-   `message_post_server`:  Imports the Flask application (`app`) to be tested.

### **Test Structure**

The code defines a class `FlaskAPITestCase` that inherits from `unittest.TestCase`. This class contains methods that define individual test cases.

1.  **`setUp(self)`**

    -   This method is a special `unittest` method that is executed before each test method.
    -   `self.app = app.test_client()`:  Creates a test client for the Flask application. The test client allows you to make requests to the application without running the server.
    -   `self.app.testing = True`:  Sets the Flask application's testing flag to `True`. This enables better error reporting during tests.

2.  **`test_create_post(self)`**

    -   This method tests the `POST /posts` endpoint, which is used to create a new post.
    -   `payload = {"subject": "UnitTest Post", "body": "Testing API post creation"}`:
        -   Defines a dictionary `payload` containing the data for the new post (subject and body).
    -   `response = self.app.post('/posts', data=json.dumps(payload), content_type='application/json')`:
        -   Uses the test client (`self.app`) to make a POST request to the `/posts` endpoint.
        -   `json.dumps(payload)`:  Serializes the `payload` dictionary into a JSON string, as this is the format expected by the API.
        -   `content_type='application/json'`:  Sets the `Content-Type` header of the request to indicate that the data is in JSON format.
    -   `self.assertEqual(response.status_code, 201)`:
        -   Asserts that the response status code is 201 (Created), which is the expected status code for a successful post creation.
        -   `self.assertEqual()` is a method provided by `unittest` to check if two values are equal. If they are not equal, the test will fail.
    -   `data = json.loads(response.data)`:
        -   Parses the JSON data from the response. `response.data` contains the response body as a byte string, and `json.loads()` converts it to a Python dictionary.
    -   `self.assertIn("id", data)`:
        -   Asserts that the response data contains an "id" field, which is the ID of the newly created post.
        -   `self.assertIn()` is another `unittest` assertion method.
    -   `self.assertEqual(data["subject"], "UnitTest Post")`:
        -   Asserts that the "subject" field in the response data matches the subject of the post that was sent in the request.

3.  **`test_get_all_posts(self)`**

    -   This method tests the `GET /posts` endpoint, which is used to retrieve all posts.
    -   `response = self.app.get('/posts')`:
        -   Makes a GET request to the `/posts` endpoint using the test client.
    -   `self.assertEqual(response.status_code, 200)`:
        -   Asserts that the response status code is 200 (OK), which is the expected status code for a successful GET request.
    -   `data = json.loads(response.data)`:
        -   Parses the JSON data from the response.
    -   `self.assertIsInstance(data, list)`:
        -   Asserts that the response data is a list, as the `GET /posts` endpoint should return a list of post objects.
        -   `self.assertIsInstance()` is a `unittest` assertion method that checks if an object is an instance of a particular class or type.

4.  **`test_update_post(self)`**

    -   This method tests the `PUT /posts/<post_id>` endpoint, which is used to update an existing post.
    -   `create_payload = {"subject": "Update Test", "body": "Original Body"}`:
        -   Defines a payload to create a post first, as you need an existing post to update.
    -   `create_response = self.app.post('/posts', data=json.dumps(create_payload), content_type='application/json')`:
        -   Creates a new post using the `POST /posts` endpoint.
    -   `post_id = json.loads(create_response.data)["id"]`:
        -   Extracts the ID of the newly created post from the response.
    -   `update_payload = {"subject": "Updated Title", "body": "Updated Body"}`:
        -   Defines a payload containing the updated data for the post.
    -   `response = self.app.put(f'/posts/{post_id}', data=json.dumps(update_payload), content_type='application/json')`:
        -   Makes a PUT request to the `/posts/{post_id}` endpoint (where `{post_id}` is replaced with the actual ID of the post).
    -   `self.assertEqual(response.status_code, 200)`:
        -   Asserts that the response status code is 200 (OK), which is the expected status code for a successful update.
    -   `updated_data = json.loads(response.data)`:
        -   Parses the JSON data from the response.
    -   `self.assertEqual(updated_data["subject"], "Updated Title")`:
        -   Asserts that the "subject" field in the response data matches the updated subject.

5.  **`test_add_comment(self)`**

    -   This method tests the `POST /posts/<post_id>/comments` endpoint, which is used to add a comment to an existing post.
    -   `create_payload = {"subject": "Comment Test", "body": "Post for comment testing"}`:
        -   Defines a payload to create a post first, as you need an existing post to add a comment to.
    -   `create_response = self.app.post('/posts', data=json.dumps(create_payload), content_type='application/json')`:
        -   Creates a new post using the `POST /posts` endpoint.
    -   `post_id = json.loads(create_response.data)["id"]`:
        -   Extracts the ID of the newly created post.
    -   `comment_payload = {"body": "This is a unittest comment"}`:
        -   Defines a payload containing the comment data.
    -   `response = self.app.post(f'/posts/{post_id}/comments', data=json.dumps(comment_payload), content_type='application/json')`:
        -   Makes a POST request to the `/posts/{post_id}/comments` endpoint.
    -   `self.assertEqual(response.status_code, 201)`:
        -   Asserts that the response status code is 201 (Created), which is the expected status code for a successful comment creation.
    -   `comment_data = json.loads(response.data)`:
        -   Parses the JSON data from the response.
    -   `self.assertEqual(comment_data["comment"]["body"], "This is a unittest comment")`:
        -   Asserts that the "body" of the created comment matches the comment data sent in the request.

6.  **`if __name__ == '__main__':`**

    -   This block ensures that the unit tests are run only when the script is executed directly (not when imported as a module).
    -   `unittest.main()`:  Runs the unit test suite. This will execute all the test methods defined in the `FlaskAPITestCase` class.

###   **How to Run the Tests**

To execute the test file, run the following command in your terminal:

### **How to Run the Tests**

To execute the test file, run the following command in your terminal:

```bash
python -m unittest test_flask_apis.py
```


## **9️⃣ `test_deployed_flask_apis.py` Explanation**

This file contains the same **unit tests** as `test_flask_apis.py`, but targets the Flask API endpoints deployed and running on **Google Cloud** instead of your local server.

To execute these tests, use the following command:

```bash
python -m unittest test_deployed_flask_apis.py
```

## **🔟 Deploying the Flask Server on Google Cloud**

To deploy the Flask server on **Google Cloud App Engine**, use the following files:

### `app.yaml`
This file configures the deployment settings for Google Cloud App Engine.

Example:

```yaml
runtime: python311

entrypoint: gunicorn -b :$PORT message_post_server:app

handlers:
  - url: /.*
    script: auto

```

### `requirements.txt`
This file lists all the dependencies needed to run the Flask application.

```bash
flask
google-cloud-firestore
gunicorn
```

### **Deployment Steps**
1. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   ```
2. **Set the active project**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```
3. **Deploy the application**:
   ```bash
   gcloud app deploy
   ```
4. **Access the deployed server**:
   ```bash
   gcloud app browse
   ```

Now your Flask server is live on Google Cloud!




