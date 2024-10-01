import sys
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from .database.models import db, setup_db, Article, Collection
from .auth.auth import requires_auth

logger.add("file.log", format="{time} - {level} - {message}")


app = Flask(__name__)
CORS(app)
setup_db(app)


@app.route("/articles/add", methods=["POST"])
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
        article_repr = repr(article)
        db.session.close()

    return jsonify({"sucess": True, "article": article_repr}), 200


@app.route("/collections/add", methods=["POST"])
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
