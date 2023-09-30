from flask_sqlalchemy import SQLAlchemy

db =  SQLAlchemy()

def connect_db(app):
    """Connecting the database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False
    )
    
    location = db.Column(
        db.Text,
        nullable=False
    )

    @classmethod
    def signup(cls, username, email, location):
        """Sign up user.

        """

        user = User(
            username=username,
            email=email,
            location=location
        )

        db.session.add(user)
        return user
