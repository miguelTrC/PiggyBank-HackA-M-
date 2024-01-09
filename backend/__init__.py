from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

""" database settings """
db:SQLAlchemy = SQLAlchemy()
DB_NAME:str = "users.db"

def create_app():
    
    """ App settings """
    app:Flask = Flask(__name__)
    app.config['SECRET_KEY'] = 'mySecret!'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    """ init app """
    db.init_app(app)

    """ Add Blueprints """
    from backend.views import authn, views

    app.register_blueprint(authn)
    app.register_blueprint(views)
    
    """ database settings """
    with app.app_context():
        db.create_all()
    
    from backend.models import AccountInfo

    """  login manager """
    login_manager = LoginManager()

    # if user not login, redirect to login page
    login_manager.login_view = 'views.index'

    # init login manager
    login_manager.init_app(app)

    """ stores user id in a session. It will get the id from the database
    using the id passed as argument"""
    @login_manager.user_loader
    def load_user(_id):
        return AccountInfo.query.get(int(_id))

    return app
