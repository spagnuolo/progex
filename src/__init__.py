from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'djfioasdfjomu0dvhiadfjcpa'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groceries.db'

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User,Household,Product,Item,Product_Category,Recipe,RecipeIngredients
    # go to /admin to see the admin view with the tables
    admin_manager = Admin()
    admin_manager.init_app(app)
    admin_manager.add_view(ModelView(User, db.session))
    admin_manager.add_view(ModelView(Household, db.session))
    admin_manager.add_view(ModelView(Product, db.session))
    admin_manager.add_view(ModelView(Item, db.session))
    admin_manager.add_view(ModelView(Product_Category, db.session))
    admin_manager.add_view(ModelView(Recipe, db.session))
    admin_manager.add_view(ModelView(RecipeIngredients, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # from .camera import camera as camera_blueprint
    # app.register_blueprint(camera_blueprint)

    return app
