import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


# Loading env vars which will be used
# in the database connection
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABSE_NAME = "myblog"
DATABASE_HOST = "localhost:5432"

database_path = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}/{DATABSE_NAME}"
)
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


articles_collections = db.Table(
    "articles_collections",
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column(
        "collection_id", db.Integer, db.ForeignKey("collections.id"), primary_key=True
    ),
)


class Article(db.Model):
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
        "Collection", secondary=articles_collections, back_populates="articles"
    )

    def __repr__(self):
        return f"<Article {self.id} : {self.title}>"


class Collection(db.Model):
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
        "Article", secondary=articles_collections, back_populates="collections"
    )

    def __repr__(self):
        return f"<Collection {self.id} : {self.title}>"
