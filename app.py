# app.py
from flask import Flask
from extensions import db, login_manager
from routes import routes 

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SESSION_PERMANENT'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'routes.login'  

# Register the routes blueprint
app.register_blueprint(routes)

# Run database setup and preload data within app context
with app.app_context():
    from models import User, Category
    db.create_all()

    # Preload users
    if User.query.count() == 0:
        users = [
            User(username='mcdavid', password='12345'),
            User(username='draisaitl', password='67890'),
            User(username='bouchard', password='24345'),
            User(username='pickard', password='12347'),
            User(username='nugent-hopkins', password='56790')
        ]
        db.session.add_all(users)
        db.session.commit()

    # Preload categories
    if Category.query.count() == 0:
        categories = [
            Category(name='Game Recaps'),
            Category(name='Comedy'),
            Category(name='Rumors'),
            Category(name='Strategies')
        ]
        db.session.add_all(categories)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)