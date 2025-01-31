#app/booking/__init__.py

from flask import Blueprint 

bp = Blueprint('booking', __name__, url_prefix='/booking')

from app.booking import routes