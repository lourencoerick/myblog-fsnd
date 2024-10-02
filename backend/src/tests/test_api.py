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
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABSE_NAME = "test_db"
DATABASE_HOST = "localhost:5432"


class MyBlogTestCase(unittest.TestCase):
    """This class represents the API test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_path = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}/{DATABSE_NAME}"
        self.app = create_app(
            {
                "TESTING": True,  # Enable test mode
                "SQLALCHEMY_DATABASE_URI": self.database_path,  # "sqlite:///:memory:",  # In-memory DB for testing
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

    def tearDown(self):
        """Executed after each test"""
        pass

    # Test POST /articles
    def test_create_article(self):
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

    # Test GET /articles
    def test_get_articles(self):
        res = self.client().get("/articles", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(len(data["articles"]))

    # Test GET /articles/<int:article_id>
    def test_get_article(self):
        res = self.client().get("/articles/1", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["article"])

    # Test PATCH /articles/<int:article_id>
    def test_update_article(self):
        updated_article = {
            "title": "Updated Article",
            "content": "Updated content",
            "author": "Updated Author",
        }
        res = self.client().patch(
            "/articles/1", json=updated_article, headers=self.valid_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["id"])

    # Test POST /collections
    def test_create_collection(self):
        new_collection = {
            "title": "New Collection",
            "description": "Description of the new collection",
            "article_ids": [1],
        }
        res = self.client().post(
            "/collections", json=new_collection, headers=self.valid_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["article"])

    # Test GET /collections
    def test_get_collections(self):
        res = self.client().get("/collections", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(len(data["collections"]))

    # Test GET /collections/<int:collection_id>
    def test_get_collection(self):
        res = self.client().get("/collections/1", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["collection"])

    # Test PATCH /collections/<int:collection_id>
    def test_update_collection(self):
        updated_collection = {
            "title": "Updated Collection",
            "description": "Updated description",
            "article_ids": [1],
        }
        res = self.client().patch(
            "/collections/1", json=updated_collection, headers=self.valid_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["sucess"])
        self.assertTrue(data["id"])

    # Test DELETE /collections/<int:collection_id>
    def test_delete_collection(self):
        res = self.client().delete("/collections/1", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["delete"])

    # Test DELETE /articles/<int:article_id>
    def test_delete_article(self):
        res = self.client().delete("/articles/1", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["delete"])

    # Test GET /articles/<int:article_id> (Fail Case - Article Not Found)
    def test_get_article_not_found(self):
        res = self.client().get("/articles/1000", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # Test POST /articles (Fail Case - Missing Authorization)
    def test_create_article_no_auth(self):
        new_article = {
            "title": "New Article",
            "content": "Content of the new article",
            "author": "Author Name",
        }
        res = self.client().post(
            "/articles", json=new_article, headers=self.no_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Test DELETE /articles/<int:article_id> (Fail Case - Article Not Found)
    def test_delete_article_not_found(self):
        res = self.client().delete("/articles/1000", headers=self.valid_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # Test DELETE /articles/<int:article_id> (Fail Case - Unauthorized no permission)
    def test_delete_article_invalid_token(self):
        res = self.client().delete(
            "/articles/1", headers=self.valid_no_credentials_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    # Test PATCH /articles/<int:article_id> (Fail Case - Missing Authorization)
    def test_update_article_no_auth(self):
        updated_article = {
            "title": "Updated Article",
            "content": "Updated content",
            "author": "Updated Author",
        }
        res = self.client().patch(
            "/articles/1", json=updated_article, headers=self.no_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
