"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg"


class User (db.Model):

    __tablename__ = 'users'


    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
        
    first_name = db.Column(db.Text,
                            nullable = False)
        
    last_name = db.Column(db.Text,
                            nullable = False)
        
        
    image_url = db.Column(db.Text,
                          nullable = False,
                          default = DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
         return f"{self.first_name} {self.last_name}"
    
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)