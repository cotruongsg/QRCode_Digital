"""Models for Playlist app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()
bcrypt = Bcrypt()

############################## USER Table #######################################
class USER(db.Model):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), nullable=False)   
   
    images = db.relationship('QRC_IMAGES_DB', backref="users", cascade='all, delete-orphan')

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

###################### QR Code Images Table ################################
class QRC_IMAGES_DB(db.Model):
    """An individual QR Code"""

    __tablename__ = 'qrcodeimages'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
         db.String(20),nullable=False,
    )

    description = db.Column(
        db.String(140),
        nullable=False,
    )    

    web_url = db.Column(
        db.String(150),nullable=False,
    )

    module_shape = db.Column(
        db.String(20),nullable=False,
    )

    module_color = db.Column(
        db.String(20),nullable=False,
    )

    inner_eye_shape = db.Column(
        db.String(20),nullable=False,
    )

    inner_eye_color = db.Column(
        db.String(20),nullable=False,
    )

    outer_eye_shape = db.Column(
        db.String(20),nullable=False,
    )

    outer_eye_color = db.Column(
        db.String(20),nullable=False,
    )

    image = db.Column(db.LargeBinary)

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id') , 
        nullable=False,
    )




############################# CREATE TABLES #######################################
# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
 
    # Create tables
    with app.app_context():        
        db.create_all()
        
      