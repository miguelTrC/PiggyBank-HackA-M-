from flask import Blueprint

""" Add blueprints here """
authn = Blueprint('authn', __name__)
views = Blueprint('views', __name__)

from backend.views import auth, routes