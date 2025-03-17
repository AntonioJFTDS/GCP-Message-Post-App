import unittest
import json
import requests

class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://crystalloids-candidates.ew.r.appspot.com"

    def test_create_post(self):
        payload = {"subject": "UnitTest Post", "body": "Testing API post creation"}
        response = requests.post(f'{self.base_url}/posts', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["subject"], "UnitTest Post")

    def test_get_all_posts(self):
        response = requests.get(f'{self.base_url}/posts')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_update_post(self):
        create_payload = {"subject": "Update Test", "body": "Original Body"}
        create_response = requests.post(f'{self.base_url}/posts', json=create_payload)
        post_id = create_response.json()["id"]

        update_payload = {"subject": "Updated Title", "body": "Updated Body"}
        response = requests.put(f'{self.base_url}/posts/{post_id}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        updated_data = response.json()
        self.assertEqual(updated_data["subject"], "Updated Title")

    def test_add_comment(self):
        create_payload = {"subject": "Comment Test", "body": "Post for comment testing"}
        create_response = requests.post(f'{self.base_url}/posts', json=create_payload)
        post_id = create_response.json()["id"]

        comment_payload = {"body": "This is a unittest comment"}
        response = requests.post(f'{self.base_url}/posts/{post_id}/comments', json=comment_payload)
        self.assertEqual(response.status_code, 201)
        comment_data = response.json()
        self.assertEqual(comment_data["comment"]["body"], "This is a unittest comment")

if __name__ == '__main__':
    unittest.main()
