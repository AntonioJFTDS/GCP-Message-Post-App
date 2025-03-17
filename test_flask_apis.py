import unittest
import json
from message_post_server import app


class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_post(self):
        payload = {"subject": "UnitTest Post", "body": "Testing API post creation"}
        response = self.app.post('/posts', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)
        self.assertEqual(data["subject"], "UnitTest Post")

    def test_get_all_posts(self):
        response = self.app.get('/posts')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_update_post(self):
        create_payload = {"subject": "Update Test", "body": "Original Body"}
        create_response = self.app.post('/posts', data=json.dumps(create_payload), content_type='application/json')
        post_id = json.loads(create_response.data)["id"]

        update_payload = {"subject": "Updated Title", "body": "Updated Body"}
        response = self.app.put(f'/posts/{post_id}', data=json.dumps(update_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        updated_data = json.loads(response.data)
        self.assertEqual(updated_data["subject"], "Updated Title")

    def test_add_comment(self):
        create_payload = {"subject": "Comment Test", "body": "Post for comment testing"}
        create_response = self.app.post('/posts', data=json.dumps(create_payload), content_type='application/json')
        post_id = json.loads(create_response.data)["id"]

        comment_payload = {"body": "This is a unittest comment"}
        response = self.app.post(f'/posts/{post_id}/comments', data=json.dumps(comment_payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        comment_data = json.loads(response.data)
        self.assertEqual(comment_data["comment"]["body"], "This is a unittest comment")


if __name__ == '__main__':
    unittest.main()
