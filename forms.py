"""Forms for playlist app."""

from wtforms import FileField , SelectField, StringField, IntegerField , BooleanField , PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired , URL , Email , Length , ValidationError
from urllib.parse import urlparse

class LogoField(FileField):
    def __init__(self, label='', validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)

    def pre_validate(self, form):
        super().pre_validate(form)
        if self.data:
            file_ext = self.data.filename.rsplit('.', 1)[-1].lower()
            allowed_extensions = {'jpg', 'jpeg', 'png'}
            if file_ext not in allowed_extensions:
                raise ValidationError('Invalid file format. Only JPG, JPEG, PNG, are allowed.')


class QRCodeForm(FlaskForm):
    data = StringField('URL', validators=[InputRequired(), URL()])
    body = StringField('QRCode_Format', validators=[InputRequired()])
    logo = LogoField('Logo', validators=[InputRequired(), URL()])
    size = IntegerField('Size', validators=[InputRequired()])
    download = BooleanField('Download')
    file = SelectField('OutputFile', choices=[('svg', 'SVG'), ('png', 'PNG')], validators=[InputRequired()])


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First_Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last_Name', validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])