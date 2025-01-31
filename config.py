# /config.py

from os import environ
from dotenv import load_dotenv
import secrets

# loading from .env

load_dotenv()

class Config:
    # generate secret key if the secret key is not set in the environment variable
    
    SECRET_KEY = environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or \
        'postgresql://postgres:password@localhost:5432/backend_sys'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False