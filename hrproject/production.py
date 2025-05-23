from .settings import *
import os

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True
