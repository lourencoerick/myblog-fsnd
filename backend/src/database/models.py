"""
Database Setup and Models for MyBlog Application

This module handles the setup of the SQLAlchemy database for the MyBlog application,
including configuration, initialization, and table creation. It defines the 
data models for articles and collections, along with their relationships, 
and provides methods for database operations such as insertion, updating, 
and deletion of records.

Key functionalities include:
- Loading environment variables for database connection.
- Setting up the database for the Flask application.
- Creating and managing many-to-many relationships between articles and collections.
- Methods for CRUD operations on articles and collections.

Classes:
- Article: Represents an article with title, content, author, and timestamps.
- Collection: Represents a collection of articles with a title and description.

Functions:
- setup_db(app, db_path): Configures and initializes the database for the Flask app.
- db_drop_and_create_all(): Drops all tables and recreates them with demo data.
"""

import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


# Loading env vars which will be used
# in the database connection
load_dotenv()

database_path = os.getenv("DATABASE_URL")
db = SQLAlchemy()


def setup_db(app, db_path=database_path):
    """
    Sets up the database for the given Flask application.

    This function configures the SQLAlchemy settings for the provided Flask app,
    initializes the database with the app context, and creates all the database tables.

    Parameters:
        app (Flask): The Flask application instance to configure for database access.
        db_path (str, optional): The database URI to connect to.
            Defaults to the value of `database_path`.
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


def db_drop_and_create_all():
    """
    Drops all existing tables and creates new ones for the database.

    This function is useful for resetting the database state during development or testing.
    It also adds one demo article and one demo collection to the database to facilitate
    testing with sample data.
    """
    db.drop_all()
    db.create_all()

    # add one demo row which is helping in POSTMAN test
    article = Article(title="water", content="about water", author="me")
    article.insert()

    collection = Collection(
        title="my water collection", description="about water and water"
    )
    article.insert()
    collection.articles.extend([article])
    collection.insert()


articles_collections = db.Table(
    "articles_collections",
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column(
        "collection_id", db.Integer, db.ForeignKey("collections.id"), primary_key=True
    ),
)


class Article(db.Model):
    """
    Represents an article in the MyBlog application.

    Attributes:
        id (int): The unique identifier for the article.
        title (str): The title of the article.
        content (str): The content of the article.
        author (str): The author of the article.
        created_at (datetime): The timestamp when the article was created.
        updated_at (datetime): The timestamp when the article was last updated.
        collections (list): The collections associated with the article.

    Methods:
        insert(): Adds the article to the database and commits the session.
        update(): Commits any changes made to the article.
        delete(): Removes the article from the database and commits the session.
        response(): Returns a dictionary representation of the article.
    """

    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Many-to-Many relationship with Collection
    collections = db.relationship(
        "Collection",
        secondary=articles_collections,
        back_populates="articles",
    )

    def insert(self):
        """Adds the article to the database and commits the session."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Commits any changes made to the article."""
        db.session.commit()

    def delete(self):
        """Removes the article from the database and commits the session."""
        db.session.delete(self)
        db.session.commit()

    def response(self):
        """Returns a dictionary representation of the article."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
        }

    def __repr__(self):
        return f"<Article {self.id} : {self.title}>"


class Collection(db.Model):
    """
    Represents a collection of articles in the MyBlog application.

    Attributes:
        id (int): The unique identifier for the collection.
        title (str): The title of the collection.
        description (str): A description of the collection.
        created_at (datetime): The timestamp when the collection was created.
        updated_at (datetime): The timestamp when the collection was last updated.
        articles (list): The articles associated with the collection.

    Methods:
        insert(): Adds the collection to the database and commits the session.
        update(): Commits any changes made to the collection.
        delete(): Removes the collection from the database and commits the session.
        response(): Returns a dictionary representation of the collection, including article IDs.
    """

    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Many-to-Many relationship with Article
    articles = db.relationship(
        "Article",
        secondary=articles_collections,
        back_populates="collections",
    )

    def insert(self):
        """Adds the collection to the database and commits the session."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Commits any changes made to the collection."""
        db.session.commit()

    def delete(self):
        """Removes the collection from the database and commits the session."""
        db.session.delete(self)
        db.session.commit()

    def response(self):
        """Returns a dictionary representation of the collection, including article IDs."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "article_ids": [article.id for article in self.articles],
        }

    def __repr__(self):
        return f"<Collection {self.id} : {self.title}>"
