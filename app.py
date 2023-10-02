import os

from flask import Flask, flash, redirect, render_template, url_for
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import UserForm
from models import db, connect_db, User
from current import currentWeather

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "this is my key")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# toolbar = DebugToolbarExtension(app)
app.app_context().push()
connect_db(app)

@app.route('/', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and collect their data (username, email, desired location for email reminders) and add to DB. Redirect to thanks page

    If form not valid, present form.

    If the there already is a user with that email: flash message
    and re-present form.
    """
    
    form = UserForm()

    
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                location=form.location.data
            )
            db.session.commit()
            
        except IntegrityError as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            flash("Invalid username or email, please try again", 'danger')
        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            flash("An unexpected error occurred, please try again later", 'danger')
        print(user)
        return redirect(url_for('say_thanks', user_id=user.id)) #after successful registration


    else:
        return render_template('signup.html', form=form)
    

@app.route("/thanks/<int:user_id>")
def say_thanks(user_id):
    """Thank user for registering for weather reminder"""

    user = User.query.get_or_404(user_id)
    try:
        currentWeather(user)
    except Exception as e:
        flash("An unexpected error occurred, please try again later", 'danger')
        
    return render_template("thanks.html", username = user.username)
