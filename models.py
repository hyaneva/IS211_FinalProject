# models.py
from datetime import datetime
from extensions import db, login_manager
from flask_login import UserMixin


# Category model to store post categories
class Category(db.Model):
    # Primary key for the category
    id = db.Column(db.Integer, primary_key=True)
    # Name of the category, must be unique and not nullable
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Category {self.name}>'


# User model for storing user information, extends UserMixin for Flask-Login functionality
class User(db.Model, UserMixin):
    # Primary key for the user
    id = db.Column(db.Integer, primary_key=True)
    # Username of the user, must be unique and not nullable
    username = db.Column(db.String(150), nullable=False, unique=True)
    # Password of the user, must be not nullable
    password = db.Column(db.String(150), nullable=False)


# Method to load user based on the user_id for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Post model to store blog posts created by users
class Post(db.Model):
    # Primary key for the post
    id = db.Column(db.Integer, primary_key=True)
    # Title of the post, must be not nullable
    title = db.Column(db.String(250), nullable=False)
    # Content of the post, must be not nullable
    content = db.Column(db.Text, nullable=False)
    # Foreign key linking to the user who created the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='posts')
    # Date and time the post was created, default is the current time
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Indicates whether the post is published or not
    is_published = db.Column(db.Boolean, default=True)
    # Foreign key for the category of the post (can be nullable)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    # Relationship to the Category model (many-to-one relationship)
    category = db.relationship('Category', backref='posts')

    def __repr__(self):
        return f'<Post {self.title}>'



