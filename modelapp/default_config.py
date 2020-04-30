import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
UPLOADED_FILES_DEST = os.path.join("static", "files")  # manage root folder
TMP_FILES_DEST = os.path.join("tmpfiles") # encoded files storage
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
LOG_CONFIG_FILE= "logging.conf"
