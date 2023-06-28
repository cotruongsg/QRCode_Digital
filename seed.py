from models import db, connect_db, OutLine
from app import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from secret import username_password , host_ip_port


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username_password}@{host_ip_port}/tvbqnjbu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

   # Create tables
    with app.app_context():        
        db.drop_all()
        db.create_all()

connect_db(app)

colors = ["#841839","#77352E","#D4134A",
          "#F0550A","#008000","#1C7137",
          "#4E9A69","#489EAB","#197CB3",
          "#003153","#000000","#1877F2",
          "#5133BC","#311C46","#5C366F","#D169B5"]

inner_eye_shape = ["circle","cushion","default",
                   "diamond","dots","heavyround",
                   "horizontal_lines","shield","star",
                   "vertical_lines"]

outer_eye_shape = ["circle","diamond","dots",
                   "heavyround","horizontal_lines","leaf",
                   "shield","left_eye","vertical_lines",
                   "lightround"]


QROutLine = [
    OutLine(
        module_shape = "heart", 
        module_color = colors , 
        inner_eye_shape = inner_eye_shape , 
        inner_eye_color = colors ,
        outer_eye_shape = outer_eye_shape , 
        outer_eye_color = colors,
    ),
    OutLine(
        module_shape = "horizontal_lines", 
        module_color = colors , 
        inner_eye_shape = inner_eye_shape , 
        inner_eye_color = colors ,
        outer_eye_shape = outer_eye_shape , 
        outer_eye_color = colors,
    ),
    OutLine(
        module_shape = "lightround", 
        module_color = colors , 
        inner_eye_shape = inner_eye_shape , 
        inner_eye_color = colors ,
        outer_eye_shape = outer_eye_shape , 
        outer_eye_color = colors,
    ),
    OutLine(
        module_shape = "classic", 
        module_color = colors , 
        inner_eye_shape = inner_eye_shape , 
        inner_eye_color = colors ,
        outer_eye_shape = outer_eye_shape , 
        outer_eye_color = colors,
    ),
    OutLine(
        module_shape = "circle", 
        module_color = colors , 
        inner_eye_shape = inner_eye_shape , 
        inner_eye_color = colors ,
        outer_eye_shape = outer_eye_shape , 
        outer_eye_color = colors,
    ),
    OutLine(
        module_shape = "vertical_lines", 
        module_color = colors , 
        inner_eye_shape = inner_eye_shape , 
        inner_eye_color = colors ,
        outer_eye_shape = outer_eye_shape , 
        outer_eye_color = colors,
    ),
]

with app.app_context():
    db.session.add_all(QROutLine)
    db.session.commit()