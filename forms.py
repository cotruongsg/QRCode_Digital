"""Forms for playlist app."""

from wtforms import FileField , SelectField, StringField, FileField , IntegerField , BooleanField , PasswordField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
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


module_shapes = ["heart","horizontal_lines","lightround",
                "classic","circle","vertical_lines"]

colors = ["#841839","#77352E","#D4134A",
          "#F0550A","#008000","#1C7137",
          "#4E9A69","#489EAB","#197CB3",
          "#003153","#000000","#1877F2",
          "#5133BC","#311C46","#5C366F","#D169B5"]

inner_eye_shapes = ["circle","cushion","default",
                "diamond","dots","heavyround",
                "horizontal_lines","shield","star",
                "vertical_lines"]

outer_eye_shapes = ["circle","diamond","dots",
                "heavyround","horizontal_lines","leaf",
                "shield","left_eye","vertical_lines",
                "lightround"]


class QRCodeForm(FlaskForm):
    data = StringField('URL', validators=[InputRequired(), URL()])
    module_shape = SelectField('Module_Shape', choices=[(module_shape,module_shape) for module_shape in module_shapes])
    module_color = SelectField('Module_Color', choices=[(color,color) for color in colors])
    inner_eye_shape = SelectField('Inner_Eye_Shape', choices=[(shape,shape) for shape in inner_eye_shapes])
    inner_eye_color = SelectField('Inner_Eye_Color', choices=[(color,color) for color in colors])
    outer_eye_shape = SelectField('Outer_Eye_Shape', choices=[(shape,shape) for shape in outer_eye_shapes])
    outer_eye_color = SelectField('Outer_Eye_Shape', choices=[(color,color) for color in colors])
    # image = FileField('Select Image', validators=[InputRequired()])


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(),
                                                    Length(min=6, max=20, message='Password must be between 6 and 20 characters')])
    
    
class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])