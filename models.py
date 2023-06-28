"""Models for Playlist app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()
bcrypt = Bcrypt()

############################## USER Table #######################################
class USER(db.Model):
    
    __tablename__ = 'usersTB'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), nullable=False)   
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    qrcodeRS = db.relationship("QRCODE", backref="userBR", cascade="all,delete")

    @classmethod
    def signup(cls , username , email ,  password):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password).decode('UTF-8')
       
        user = cls(
            username = username,            
            email = email , 
            password = hashed ,         
        )
        db.session.add(user)
        return user
    
    
    @classmethod
    def authenticate(cls , username , password):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """
        user = USER.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password , password):
            return user
        else:
            return False
    


############################## Options Table ###################################
# class OutLine(db.Model):
#     """Create db to give choices to make QR Code how looks based on user select"""
#     __tablename__ = 'qrCodeOptionsTB'

#     id = db.Column(db.Integer, primary_key=True)
#     module_shape = db.Column(db.String(50))
#     module_color = db.Column(postgresql.ARRAY(db.String(7)))
#     inner_eye_shape = db.Column(postgresql.ARRAY(db.String(200)))
#     inner_eye_color = db.Column(postgresql.ARRAY(db.String(500)))
#     outer_eye_shape = db.Column(postgresql.ARRAY(db.String(200)))
#     outer_eye_color = db.Column(postgresql.ARRAY(db.String(500)))
#     image = db.Column(db.LargeBinary , nullable=True)



############################## QR Code Table ###################################
class QRCODE(db.Model):
    """An individual QR Code"""

    __tablename__ = 'qrCodeTB'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    description = db.Column(
        db.String(140),
        nullable=False,
    )

    image = db.Column(db.LargeBinary)

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('usersTB.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('USER')


############################# CREATE TABLES #######################################
# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

    # colors = ["#841839","#77352E","#D4134A",
    #       "#F0550A","#008000","#1C7137",
    #       "#4E9A69","#489EAB","#197CB3",
    #       "#003153","#000000","#1877F2",
    #       "#5133BC","#311C46","#5C366F","#D169B5"]

    # inner_eye_shape = ["circle","cushion","default",
    #                 "diamond","dots","heavyround",
    #                 "horizontal_lines","shield","star",
    #                 "vertical_lines"]

    # outer_eye_shape = ["circle","diamond","dots",
    #                 "heavyround","horizontal_lines","leaf",
    #                 "shield","left_eye","vertical_lines",
    #                 "lightround"]


    # QROutLine = [
    #     OutLine(
    #         module_shape = "heart", 
    #         module_color = colors , 
    #         inner_eye_shape = inner_eye_shape , 
    #         inner_eye_color = colors ,
    #         outer_eye_shape = outer_eye_shape , 
    #         outer_eye_color = colors,
    #     ),
    #     OutLine(
    #         module_shape = "horizontal_lines", 
    #         module_color = colors , 
    #         inner_eye_shape = inner_eye_shape , 
    #         inner_eye_color = colors ,
    #         outer_eye_shape = outer_eye_shape , 
    #         outer_eye_color = colors,
    #     ),
    #     OutLine(
    #         module_shape = "lightround", 
    #         module_color = colors , 
    #         inner_eye_shape = inner_eye_shape , 
    #         inner_eye_color = colors ,
    #         outer_eye_shape = outer_eye_shape , 
    #         outer_eye_color = colors,
    #     ),
    #     OutLine(
    #         module_shape = "classic", 
    #         module_color = colors , 
    #         inner_eye_shape = inner_eye_shape , 
    #         inner_eye_color = colors ,
    #         outer_eye_shape = outer_eye_shape , 
    #         outer_eye_color = colors,
    #     ),
    #     OutLine(
    #         module_shape = "circle", 
    #         module_color = colors , 
    #         inner_eye_shape = inner_eye_shape , 
    #         inner_eye_color = colors ,
    #         outer_eye_shape = outer_eye_shape , 
    #         outer_eye_color = colors,
    #     ),
    #     OutLine(
    #         module_shape = "vertical_lines", 
    #         module_color = colors , 
    #         inner_eye_shape = inner_eye_shape , 
    #         inner_eye_color = colors ,
    #         outer_eye_shape = outer_eye_shape , 
    #         outer_eye_color = colors,
    #     ),
    # ]


    # Create tables
    with app.app_context():        
        db.create_all()
        
        # Check if QROutLine records exist
        # if not OutLine.query.all():
            # db.session.add_all(QROutLine)
            # db.session.commit()
