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

    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get("SQLALCHEMY_DATABASE_URI")
        setup_db(app, db_path=database_path)
        with app.app_context():
            db_drop_and_create_all()

    @app.route("/articles", methods=["GET"])
    def get_articles():
        page = request.args.get("page", 1)
        articles = Article.query.paginate(page=page, per_page=ARTICLES_PER_PAGE).items

        return (
            jsonify(
                {
                    "sucess": True,
                    "articles": [article.response() for article in articles],
                }
            ),
            200,
        )

    @app.route("/articles/<int:article_id>", methods=["GET"])
    # @requires_auth(permission="")
    def get_article(article_id):

        article = Article.query.filter(Article.id == article_id).one_or_none()
        if article is None:
            abort(404, description=f"ID {id} not found")

        return (
            jsonify({"sucess": True, "article": article.response()}),
            200,
        )

    @app.route("/articles", methods=["POST"])
    @requires_auth(permission="post:articles")
    def create_article():

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
        finally:
            article_id = article.id
            db.session.close()

        return jsonify({"sucess": True, "id": article_id}), 200

    @app.route("/articles/<int:article_id>", methods=["PATCH"])
    @requires_auth(permission="patch:articles")
    def edit_article(article_id):

        body = request.get_json()
        logger.info(f"Body of the article request: {body}")

        title = body.get("title")
        content = body.get("content")
        author = body.get("author")

        article = Article.query.filter(Article.id == article_id).one_or_none()
        if article is None:
            abort(404, description=f"ID {id} not found")
        article.title = title
        article.content = content
        article.author = author

        try:
            article.update()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error trying to update an existing article, {e}")
            abort(500, description=f"Error updating data into database: {str(e)}")
        finally:
            db.session.close()

        return jsonify({"sucess": True, "id": article_id}), 200

    @app.route("/articles/<int:article_id>", methods=["DELETE"])
    @requires_auth(permission="delete:articles")
    def delete_article(article_id):
        article = Article.query.filter(Article.id == article_id).one_or_none()

        if article is None:
            abort(404, description=f"Drink ID {article_id} not found")
        try:
            article.delete()
        except SQLAlchemyError as e:
            logger.error(f"Error trying to delete an existing article, {e}")
            abort(500, description=f"Error deleting data into database: {str(e)}")

        return jsonify({"success": True, "delete": article_id}), 200

    @app.route("/collections", methods=["GET"])
    def get_collections():
        page = request.args.get("page", 1)
        collections = Collection.query.paginate(
            page=page, per_page=COLLECTION_PER_PAGE
        ).items

        return (
            jsonify(
                {
                    "sucess": True,
                    "collections": [
                        collection.response() for collection in collections
                    ],
                }
            ),
            200,
        )

    @app.route("/collections/<int:collection_id>", methods=["GET"])
    # @requires_auth(permission="")
    def get_collection(collection_id):

        collection = Collection.query.filter(
            Collection.id == collection_id
        ).one_or_none()
        if collection is None:
            abort(404, description=f"ID {id} not found")

        return (
            jsonify({"sucess": True, "collection": collection.response()}),
            200,
        )

    @app.route("/collections", methods=["POST"])
    @requires_auth(permission="post:collections")
    def create_collection():

        body = request.get_json()
        logger.info(f"Body of the article request: {body}")

        title = body.get("title")
        description = body.get("description")
        article_ids = body.get("article_ids")

        collection = Collection(title=title, description=description)

        # fetching the articles of the collection
        articles = Article.query.filter(Article.id.in_(article_ids)).all()

        try:
            collection.articles.extend(articles)
            collection.insert()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error trying to insert a new collection, {e}")
        finally:
            collection_repr = repr(collection)
            db.session.close()

        return jsonify({"sucess": True, "article": collection_repr}), 200

    @app.route("/collections/<int:collection_id>", methods=["PATCH"])
    @requires_auth(permission="patch:collections")
    def edit_collection(collection_id):

        body = request.get_json()
        logger.info(f"Body of the article request: {body}")

        title = body.get("title")
        description = body.get("description")
        article_ids = body.get("article_ids")

        collection = Collection.query.filter(
            Collection.id == collection_id
        ).one_or_none()
        if collection is None:
            abort(404, description=f"ID {id} not found")

        # fetching the articles of the collection
        articles = Article.query.filter(Article.id.in_(article_ids)).all()

        collection.title = title
        collection.description = description
        collection.articles = articles

        try:
            collection.update()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error trying to update an existing collection, {e}")
            abort(500, description=f"Error updating data into database: {str(e)}")
        finally:
            db.session.close()

        return jsonify({"sucess": True, "id": collection_id}), 200

    @app.route("/collections/<int:collection_id>", methods=["DELETE"])
    @requires_auth(permission="delete:collections")
    def delete_collection(collection_id):
        collection = Collection.query.filter(
            Collection.id == collection_id
        ).one_or_none()

        if collection is None:
            abort(404, description=f"Drink ID {collection_id} not found")
        try:
            collection.delete()
        except SQLAlchemyError as e:
            logger.error(f"Error trying to delete an existing collection, {e}")
            abort(500, description=f"Error deleting data into database: {str(e)}")

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
