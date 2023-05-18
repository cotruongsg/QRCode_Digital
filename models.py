"""Models for Playlist app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

############################## USER Table #######################################
class USER(db.Model):
    
    __tablename__ = 'usersTB'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    qrcodeRS = db.relationship("QRCODE", backref="userBR", cascade="all,delete")

    @classmethod
    def register(cls , username , password , first_name , last_name , email):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password).decode('UTF-8')
       
        user = cls(
            username = username,
            password = hashed,
            email = email ,
            first_name = first_name , 
            last_name = last_name,
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
    
############################## QR Code Table ###################################
class QRCODE(db.Model):
    """An individual QR Code"""

    __tablename__ = 'qrCodeTB'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    text = db.Column(
        db.String(140),
        nullable=False,
    )

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

    # Create tables
    with app.app_context():        
        db.create_all()