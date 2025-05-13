# routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Post, Category
from extensions import db

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)

# Home page displaying all published posts
@routes.route('/')
def index():
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

# Login page, allowing users to log in
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('routes.dashboard'))  # Redirect to dashboard after successful login
        flash('Invalid credentials')
        return render_template('login.html')  # Show login page with error if credentials are invalid

    return render_template('login.html')  # For GET request, simply show the login page

# Dashboard showing user's posts
@routes.route('/dashboard')
@login_required  # Ensure only logged-in users can access this page
def dashboard():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.id.desc()).all()
    return render_template('dashboard.html', posts= posts)

# Logout functionality
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))  # Redirect to home page after logout

# Page to create a new post
@routes.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    categories = Category.query.all()  # Fetch all categories
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form.get('category')  # Get selected category
        new_post = Post(title=title, content=content, user_id=current_user.id, category_id=category_id)
        db.session.add(new_post)
        db.session.commit()
        
        flash("Post created successfully!")
        return redirect(url_for('routes.dashboard'))  # Redirect to dashboard after post creation
    
    return render_template('create.html', categories= categories)  # Pass categories to template

# Page to edit an existing post
@routes.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    categories = Category.query.all()  # Fetch all categories
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.category_id = request.form.get('category')  # Update category
        db.session.commit()
        
        flash("Post updated successfully!")
        return redirect(url_for('routes.dashboard'))  # Redirect to dashboard after post update
    
    return render_template('edit_post.html', post=post, categories=categories)

# Delete an existing post
@routes.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash("Post deleted successfully!")
    return redirect(url_for('routes.dashboard'))  # Redirect to dashboard after deletion

# Page to view a single post
@routes.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post= post)

# Unpublish a post (set its status to unpublished)
@routes.route('/post/<int:post_id>/unpublish', methods=['POST'])
@login_required
def unpublish(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash("You don't have permission to unpublish this post.")
        return redirect(url_for('routes.dashboard'))

    post.is_published = False
    db.session.commit()
    flash('Post unpublished.')
    return redirect(url_for('routes.dashboard'))  # Redirect to dashboard after unpublishing

# Publish a post (set its status to published)
@routes.route('/post/<int:post_id>/publish', methods=['POST'])
@login_required
def publish(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash("You don't have permission to publish this post.")
        return redirect(url_for('routes.dashboard'))

    post.is_published = True
    db.session.commit()
    flash('Post published.')
    return redirect(url_for('routes.dashboard'))  # Redirect to dashboard after publishing

# View posts in a specific category
@routes.route('/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category.id).all()
    return render_template('category_posts.html', category=category, posts=posts)

# Page to create a new category
@routes.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    categories = Category.query.all()  # Fetch all categories

    if request.method == 'POST':
        category_name = request.form['category_name']
        # Check if the category already exists
        if Category.query.filter_by(name=category_name).first():
            flash('Category already exists!')
        else:
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            flash('Category created successfully!')
        return redirect(url_for('routes.create_category'))

    return render_template('create_category.html', categories=categories)  # Pass categories to template

# Delete an existing category
@routes.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    # Delete the category
    db.session.delete(category)
    db.session.commit()

    flash("Category deleted successfully!")
    return redirect(url_for('routes.create_category'))  # Redirect to category creation page after deletion
