import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")
ADMIN = os.environ.get("ADMIN", "")