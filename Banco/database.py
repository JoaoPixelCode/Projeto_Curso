from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
db = SQLAlchemy()

def init_db(app):
    load_dotenv()

    DB_URL= os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
