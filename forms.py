"""Forms for playlist app."""

from wtforms import FileField , SelectField, StringField, FileField , IntegerField , BooleanField , PasswordField , TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from wtforms.validators import InputRequired , URL , Email , Length , ValidationError
from urllib.parse import urlparse
from markupsafe import Markup
from wtforms.widgets import html_params



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


class ColorOptionWidget:
    color_names = {
        "#841839": "Maroon",
        "#77352E": "Rust",
        "#D4134A": "Crimson",
        "#F0550A": "Orange",
        "#008000": "Green",
        "#1C7137": "Forest Green",
        "#4E9A69": "Sage",
        "#489EAB": "Steel Blue",
        "#197CB3": "Dodger Blue",
        "#003153": "Midnight Blue",
        "#000000": "Black",
        "#1877F2": "Facebook Blue",
        "#5133BC": "Purple",
        "#311C46": "Dark Purple",
        "#5C366F": "Plum",
        "#D169B5": "Pink"
    }   

    def __call__(self, field, **kwargs):
        options = []
        for value, label in field.choices:
            selected = 'selected' if value == field.data else ''
            color_name = self.color_names.get(value, value)
            style = f'background-color: {value};'
            options.append(
                f'<option value="{value}" style="{style}" {selected}>{color_name}</option>'
            )
        html = '<select {}>{}</select>'.format(html_params(name=field.name, **kwargs), Markup('\n'.join(options)))
        return Markup(html)    


class QRCodeForm(FlaskForm):
    data = StringField('URL', validators=[InputRequired(), URL()])
    name = StringField('Name of QR', validators=[InputRequired()])
    description = TextAreaField('QR descriptions', validators=[InputRequired()])
    module_shape = SelectField('Module_Shapes', choices=[(module_shape,module_shape) for module_shape in module_shapes])
    module_color = SelectField('Module_Colors', choices=[], widget=ColorOptionWidget())
    inner_eye_shape = SelectField('Inner_Eye_Shapes', choices=[(shape,shape) for shape in inner_eye_shapes])
    inner_eye_color = SelectField('Inner_Eye_Colors', choices=[], widget=ColorOptionWidget())
    outer_eye_shape = SelectField('Outer_Eye_Shapes', choices=[(shape,shape) for shape in outer_eye_shapes])
    outer_eye_color = SelectField('Outer_Eye_Colors', choices=[], widget=ColorOptionWidget())
 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_color.choices = [(color, color) for color in colors]
        self.inner_eye_color.choices = [(color, color) for color in colors]
        self.outer_eye_color.choices = [(color, color) for color in colors]

    def process_data(self, value):
        if value is not None:
            self.module_color.data = value
            self.inner_eye_color.data = value
            self.outer_eye_color.data = value 


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(),
                                                    Length(min=6, max=20, message='Password must be between 6 and 20 characters')])
    
    
class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])