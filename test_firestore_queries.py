import unittest
from google.cloud import firestore
from firestore_queries import insert_post, get_all_posts, get_post, update_post, add_comment, update_comment
import datetime

class FirestoreTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize Firestore client before running tests"""
        cls.db = firestore.Client(database="antoniodb")
        cls.collection_name = "collection_posts"
        cls.test_author = "test_user@gmail.com"
        cls.test_subject = "Test Post"
        cls.test_body = "This is a test post."
        
        # Insert a test post
        cls.test_post_id = insert_post(cls.test_author, cls.test_subject, cls.test_body)
        
    def test_get_all_posts(self):
        """Test retrieving all posts"""
        posts = get_all_posts()
        self.assertGreater(len(posts), 0)

    def test_get_post(self):
        """Test retrieving a specific post by ID"""
        post = get_post(self.test_post_id)
        self.assertIsNotNone(post)
        self.assertEqual(post["subject"], self.test_subject)

    def test_update_post(self):
        """Test updating a post"""
        new_subject = "Updated Post"
        new_body = "Updated post body."
        update_post(self.test_post_id, new_subject, new_body)
        updated_post = get_post(self.test_post_id)
        self.assertEqual(updated_post["subject"], new_subject)
        self.assertEqual(updated_post["body"], new_body)
    
    def test_add_comment(self):
        """Test adding a comment to a post"""
        comment_author = "commenter@gmail.com"
        comment_body = "This is a test comment."
        add_comment(self.test_post_id, comment_author, comment_body)
        updated_post = get_post(self.test_post_id)
        self.assertGreater(len(updated_post["comments"]), 0)
    
    def test_update_comment(self):
        """Test updating a comment"""
        updated_body = "Updated comment body."
        updated_post = get_post(self.test_post_id)
        if updated_post["comments"]:
            first_comment = updated_post["comments"][0]
            update_comment(self.test_post_id, first_comment["creation_date"], updated_body)
            updated_post = get_post(self.test_post_id)
            self.assertEqual(updated_post["comments"][0]["body"], updated_body)
        else:
            self.fail("No comment found to update")
    
    def test_invalid_post_id(self):
        """Test querying with an invalid post ID"""
        with self.assertRaises(ValueError):
            get_post("invalid_post_id")

    def test_update_nonexistent_post(self):
        """Test updating a non-existent post"""
        with self.assertRaises(ValueError):
            update_post("invalid_post_id", "New Subject", "New Body")
    
    def test_add_comment_invalid_post(self):
        """Test adding a comment to a non-existent post"""
        with self.assertRaises(ValueError):
            add_comment("invalid_post_id", "commenter@gmail.com", "Test comment")
    
    def test_update_nonexistent_comment(self):
        """Test updating a non-existent comment"""
        with self.assertRaises(ValueError):
            update_comment(self.test_post_id, "nonexistent_creation_date", "Updated Body")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test data"""
        cls.db.collection(cls.collection_name).document(cls.test_post_id).delete()
        print("Test data cleaned up.")

if __name__ == "__main__":
    unittest.main()
