# IS211_FinalProject

# Flask Blog App

This project is a simple blog application built using Flask. It allows users to register, log in, create, edit, and view blog posts. Each post can be assigned to a category, which helps in organizing and filtering content. Users can also create new categories through the interface. The home page displays all published posts, while the dashboard shows the logged-in user's own posts with options to edit, delete, publish, or unpublish them.

## How It Works

The application is structured using Flask Blueprints for clean routing. The main files include:

- `app.py`: Initializes the Flask app and integrates routes, database, and extensions.
- `extensions.py`: Sets up Flask extensions like SQLAlchemy and Flask-Login.
- `models.py`: Defines SQLAlchemy models for `User`, `Post`, and `Category`, establishing relationships between them.
- `routes.py`: Contains route logic for post management, category filtering, user login/logout, and post publishing.

Templates are stored in the `templates/` folder and render forms for creating and editing posts, as well as views for listing posts by category or user.

## Data Model

- `User`: Stores username and password fields (not encrypted, but definitely should be in real scenarios).
- `Post`: Includes fields for title, content, creation date, publishing status, user ID, and category ID. It is linked to the `User` and `Category` models via foreign keys.
- `Category`: Stores a unique name for the category. Posts are assigned to categories using a one-to-many relationship.

## Running the App

1. Clone the repository.
2. Make sure you have Python and Flask installed.
3. Run the app using:
   ```bash
   python app.py
