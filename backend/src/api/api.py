"""
This module provides the Flask application for managing articles and collections.

It defines the API endpoints for creating, reading, updating,
and deleting articles and collections,
with integrated authentication and error handling. 
The application uses SQLAlchemy for database interactions,
and it supports pagination for retrieving lists of articles and collections.

Usage:
To run the application, create an instance using the `create_app()` function 
and configure the necessary
environment settings for the database connection and authentication.
"""

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from src.database.models import (
    db,
    setup_db,
    db_drop_and_create_all,
    Article,
    Collection,
)
from src.auth.auth import requires_auth

logger.add("file.log", format="{time} - {level} - {message}")

ARTICLES_PER_PAGE = 1000
COLLECTION_PER_PAGE = 1000


def create_app(test_config=None):
    """
    Create and configure the Flask application.

    This function sets up the Flask app, including CORS, database configuration,
    and initializes the app context. It also defines the API routes for handling
    articles and collections.

    Parameters:
        test_config (dict, optional): A dictionary containing test configuration.
            If provided, it will set up the app with the specified database URI.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get("SQLALCHEMY_DATABASE_URI")
        setup_db(app, db_path=database_path)
        with app.app_context():
            db_drop_and_create_all()

    @app.route("/api/articles", methods=["GET"])
    def get_articles():
        """
        Retrieve a paginated list of articles.

        Query parameters:
            page (int): The page number for pagination (default is 1).

        Returns:
            tuple: A JSON response containing a success status and the list of articles.
        """
        page = request.args.get("page", 1)
        articles = Article.query.paginate(page=page, per_page=ARTICLES_PER_PAGE).items

        return (
            jsonify(
                {
                    "success": True,
                    "articles": [article.response() for article in articles],
                }
            ),
            200,
        )

    @app.route("/api/articles/<int:article_id>", methods=["GET"])
    def get_article(article_id):
        """
        Retrieve a specific article by its ID.

        Parameters:
            article_id (int): The ID of the article to retrieve.

        Returns:
            tuple: A JSON response containing a success status and the article.
        """
        article = Article.query.filter(Article.id == article_id).one_or_none()
        if article is None:
            abort(404, description=f"ID {article_id} not found")

        return (
            jsonify({"success": True, "article": article.response()}),
            200,
        )

    @app.route("/api/articles", methods=["POST"])
    @requires_auth(permission="post:articles")
    def create_article():
        """
        Create a new article.

        Returns:
            tuple: A JSON response containing a success status and the ID of the created article.
        """
        body = request.get_json()
        logger.info(f"Body of the article request: {body}")

        title = body.get("title")
        content = body.get("content")
        author = body.get("author")

        article = Article(title=title, content=content, author=author)

        try:
            article.insert()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error trying to insert a new article, {e}")
            abort(500, description="Error inserting new article.")
        finally:
            article_id = article.id
            db.session.close()

        return jsonify({"success": True, "id": article_id}), 200

    @app.route("/api/articles/<int:article_id>", methods=["PATCH"])
    @requires_auth(permission="patch:articles")
    def edit_article(article_id):
        """
        Update an existing article.

        Parameters:
            article_id (int): The ID of the article to update.

        Returns:
            tuple: A JSON response containing a success status and the ID of the updated article.
        """
        body = request.get_json()
        logger.info(f"Body of the article request: {body}")

        title = body.get("title")
        content = body.get("content")
        author = body.get("author")

        article = Article.query.filter(Article.id == article_id).one_or_none()
        if article is None:
            abort(404, description=f"ID {article_id} not found")

        article.title = title
        article.content = content
        article.author = author

        try:
            article.update()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error trying to update an existing article, {e}")
            abort(500, description="Error updating article.")
        finally:
            db.session.close()

        return jsonify({"success": True, "id": article_id}), 200

    @app.route("/api/articles/<int:article_id>", methods=["DELETE"])
    @requires_auth(permission="delete:articles")
    def delete_article(article_id):
        """
        Delete an article by its ID.

        Parameters:
            article_id (int): The ID of the article to delete.

        Returns:
            tuple: A JSON response containing a success status and the ID of the deleted article.
        """
        article = Article.query.filter(Article.id == article_id).one_or_none()

        if article is None:
            abort(404, description=f"Article ID {article_id} not found")

        try:
            article.delete()
        except SQLAlchemyError as e:
            logger.error(f"Error trying to delete an existing article, {e}")
            abort(500, description="Error deleting article.")

        return jsonify({"success": True, "delete": article_id}), 200

    @app.route("/api/collections", methods=["GET"])
    def get_collections():
        """
        Retrieve a paginated list of collections.

        Query parameters:
            page (int): The page number for pagination (default is 1).

        Returns:
            tuple: A JSON response containing a success status and the list of collections.
        """
        page = request.args.get("page", 1)
        collections = Collection.query.paginate(
            page=page, per_page=COLLECTION_PER_PAGE
        ).items

        return (
            jsonify(
                {
                    "success": True,
                    "collections": [
                        collection.response() for collection in collections
                    ],
                }
            ),
            200,
        )

    @app.route("/api/collections/<int:collection_id>", methods=["GET"])
    def get_collection(collection_id):
        """
        Retrieve a specific collection by its ID.

        Parameters:
            collection_id (int): The ID of the collection to retrieve.

        Returns:
            tuple: A JSON response containing a success status and the collection.
        """
        collection = Collection.query.filter(
            Collection.id == collection_id
        ).one_or_none()
        if collection is None:
            abort(404, description=f"ID {collection_id} not found")

        return (
            jsonify({"success": True, "collection": collection.response()}),
            200,
        )

    @app.route("/api/collections", methods=["POST"])
    @requires_auth(permission="post:collections")
    def create_collection():
        """
        Create a new collection.

        Returns:
            tuple: A JSON response containing a success status and the ID of the created collection.
        """
        body = request.get_json()
        logger.info(f"Body of the collection request: {body}")

        title = body.get("title")
        description = body.get("description")
        article_ids = body.get("article_ids")

        collection = Collection(title=title, description=description)

        # Fetching the articles of the collection
        if article_ids is not None:
            articles = Article.query.filter(Article.id.in_(article_ids)).all()
            collection.articles.extend(articles)
        try:
            collection.insert()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error trying to insert a new collection, {e}")
            abort(500, description="Error inserting new collection.")
        finally:
            collection_id = collection.id
            db.session.close()

        return jsonify({"success": True, "id": collection_id}), 200

    @app.route("/api/collections/<int:collection_id>", methods=["PATCH"])
    @requires_auth(permission="patch:collections")
    def edit_collection(collection_id):
        """
        Update an existing collection.

        Parameters:
            collection_id (int): The ID of the collection to update.

        Returns:
            tuple: A JSON response containing a success status and the ID of the updated collection.
        """
        body = request.get_json()
        logger.info(f"Body of the collection request: {body}")

        title = body.get("title")
        description = body.get("description")
        article_ids = body.get("article_ids")

        collection = Collection.query.filter(
            Collection.id == collection_id
        ).one_or_none()
        if collection is None:
            abort(404, description=f"ID {collection_id} not found")

        # Fetching the articles of the collection
        articles = Article.query.filter(Article.id.in_(article_ids)).all()

        collection.title = title
        collection.description = description
        collection.articles = articles

        try:
            collection.update()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error trying to update an existing collection, {e}")
            abort(500, description="Error updating collection.")
        finally:
            db.session.close()

        return jsonify({"success": True, "id": collection_id}), 200

    @app.route("/api/collections/<int:collection_id>", methods=["DELETE"])
    @requires_auth(permission="delete:collections")
    def delete_collection(collection_id):
        """
        Delete a collection by its ID.

        Parameters:
            collection_id (int): The ID of the collection to delete.

        Returns:
            tuple: A JSON response containing a success status and the ID of the deleted collection.
        """
        collection = Collection.query.filter(
            Collection.id == collection_id
        ).one_or_none()

        if collection is None:
            abort(404, description=f"Collection ID {collection_id} not found")

        try:
            collection.delete()
        except SQLAlchemyError as e:
            logger.error(f"Error trying to delete an existing collection, {e}")
            abort(500, description="Error deleting collection.")

        return jsonify({"success": True, "delete": collection_id}), 200

    @app.errorhandler(401)
    def request_malformed_authorization(error):
        description = getattr(
            error, "description", "Request lacks authorization parameter"
        )
        return jsonify({"success": False, "error": 401, "message": description}), 401

    @app.errorhandler(403)
    def unauthorized(error):
        description = getattr(error, "description", "Unauthorized")
        return jsonify({"success": False, "error": 403, "message": description}), 403

    @app.errorhandler(404)
    def not_found(error):
        description = getattr(error, "description", "not found")
        return jsonify({"success": False, "error": 404, "message": description}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        description = getattr(error, "description", "unprocessable")
        return jsonify({"success": False, "error": 422, "message": description}), 422

    @app.errorhandler(500)
    def crud_request_error(error):
        description = getattr(error, "description", "Error processing the request")
        return jsonify({"success": False, "error": 500, "message": description}), 500

    @app.errorhandler(400)
    def jwt_lacks_permissions(error):
        description = getattr(error, "description", "Permissions are not in JWT")
        return jsonify({"success": False, "error": 400, "message": description}), 400

    return app
