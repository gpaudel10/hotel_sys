#app/auth/__init__.py

from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

 # import routes after creating blueprint
 
from app.auth import routes 


