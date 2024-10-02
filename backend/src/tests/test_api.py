"""
MyBlog API Test Module

This module contains unit tests for the MyBlog API, built using Flask. It includes test cases
for various endpoints related to articles and collections, ensuring that the API behaves
correctly under different conditions, including successful operations and error handling.

The tests cover the following functionalities:
- Creating, retrieving, updating, and deleting articles.
- Creating, retrieving, updating, and deleting collections.
- Authorization checks with valid and invalid tokens.
- Handling of error cases such as missing authorization and not found resources.

Environment variables are used to configure the test database and authorization tokens.
"""

import unittest
import json
import os
from dotenv import load_dotenv

from src.api.api import create_app

# Loading env vars which will be used
# in the database connection
load_dotenv()
VALID_AUTH0_TOKEN = os.getenv("VALID_AUTH0_TOKEN")
VALID_NO_ROLE_AUTH0_TOKEN = os.getenv("VALID_NO_ROLE_AUTH0_TOKEN")
DATABASE_URL = os.getenv("TEST_DATABASE_URL")


class MyBlogTestCase(unittest.TestCase):
    """This class represents the API test case"""

    def setUp(self):
        """Define test variables and initialize the app."""
        self.database_path = DATABASE_URL
        self.app = create_app(
            {
                "TESTING": True,  # Enable test mode
                "SQLALCHEMY_DATABASE_URI": self.database_path,
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            }
        )
        self.client = self.app.test_client

        # Tokens with different permissions and missing/invalid tokens
        self.valid_auth_header = {"Authorization": f"Bearer {VALID_AUTH0_TOKEN}"}
        self.invalid_auth_header = {"Authorization": f"Bearer {VALID_AUTH0_TOKEN}l"}
        self.valid_no_credentials_auth_header = {
            "Authorization": f"Bearer {VALID_NO_ROLE_AUTH0_TOKEN}"
        }

        self.no_auth_header = {}

    def test_create_article(self):
        """Test the creation of a new article."""
        new_article = {
            "title": "New Article",
            "content": "Content of the new article",
            "author": "Author Name",
        }
        res = self.client().post(
            "/articles", json=new_article, headers=self.valid_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["id"])

    def test_get_articles(self):
        """Test retrieving a list of articles."""
        res = self.client().get("/api/articles", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(len(data["articles"]))

    def test_get_article(self):
        """Test retrieving a specific article by its ID."""
        res = self.client().get("/api/articles/1", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["article"])

    def test_update_article(self):
        """Test updating an existing article."""
        updated_article = {
            "title": "Updated Article",
            "content": "Updated content",
            "author": "Updated Author",
        }
        res = self.client().patch(
            "/api/articles/1", json=updated_article, headers=self.valid_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["id"])

    def test_create_collection(self):
        """Test the creation of a new collection."""
        new_collection = {
            "title": "New Collection",
            "description": "Description of the new collection",
            "article_ids": [1],
        }
        res = self.client().post(
            "/api/collections", json=new_collection, headers=self.valid_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["article"])

    def test_get_collections(self):
        """Test retrieving a list of collections."""
        res = self.client().get("/api/collections", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(len(data["collections"]))

    def test_get_collection(self):
        """Test retrieving a specific collection by its ID."""
        res = self.client().get("/api/collections/1", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["collection"])

    def test_update_collection(self):
        """Test updating an existing collection."""
        updated_collection = {
            "title": "Updated Collection",
            "description": "Updated description",
            "article_ids": [1],
        }
        res = self.client().patch(
            "/api/collections/1",
            json=updated_collection,
            headers=self.valid_auth_header,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["id"])

    def test_delete_collection(self):
        """Test deleting a specific collection by its ID."""
        res = self.client().delete("/api/collections/1", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["delete"])

    def test_delete_article(self):
        """Test deleting a specific article by its ID."""
        res = self.client().delete("/api/articles/1", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["delete"])

    def test_get_article_not_found(self):
        """Test getting an article that does not exist (404 error)."""
        res = self.client().get("/api/articles/1000", headers=self.valid_auth_header)
        self.assertEqual(res.status_code, 404)

    def test_create_article_no_auth(self):
        """Test creating an article without authorization (401 error)."""
        new_article = {
            "title": "New Article",
            "content": "Content of the new article",
            "author": "Author Name",
        }
        res = self.client().post(
            "/api/articles", json=new_article, headers=self.no_auth_header
        )
        self.assertEqual(res.status_code, 401)

    def test_delete_article_not_found(self):
        """Test deleting an article that does not exist (404 error)."""
        res = self.client().delete("/api/articles/1000", headers=self.valid_auth_header)
        self.assertEqual(res.status_code, 404)

    def test_delete_article_invalid_token(self):
        """Test deleting an article with an invalid token (403 error)."""
        res = self.client().delete(
            "/api/articles/1", headers=self.valid_no_credentials_auth_header
        )
        self.assertEqual(res.status_code, 403)

    def test_update_article_no_auth(self):
        """Test updating an article without authorization (401 error)."""
        updated_article = {
            "title": "Updated Article",
            "content": "Updated content",
            "author": "Updated Author",
        }
        res = self.client().patch(
            "/api/articles/1", json=updated_article, headers=self.no_auth_header
        )
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
