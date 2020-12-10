from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class RegisterForm(FlaskForm):
    """Form for adding Users"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=120)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=120)],
    )
   

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=120)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=120)],
    )

    