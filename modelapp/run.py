
import os
from flask_migrate import Migrate
from db import db
from ma import ma
from app import app

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)