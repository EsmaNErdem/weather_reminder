from flask_wtf import FlaskForm 
from wtforms import StringField
from wtforms.validators import InputRequired, Length, Email


class UserForm(FlaskForm):
    """Form for adding users."""
    
    username = StringField(
        "Username", 
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    email = StringField(
        "Email", 
        validators=[InputRequired(), Email()],
    )
    location = StringField(
        'Town, State', 
        validators=[InputRequired()]
    )