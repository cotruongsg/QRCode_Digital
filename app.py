import requests
from flask import Flask, redirect, render_template , flash , g , session , request , url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, USER 
from forms import QRCodeForm , SignUpForm , LoginForm 
from sqlalchemy.exc import IntegrityError
from secret import username_password , host_ip_port
import base64
from io import BytesIO
from PIL import Image
# import cairosvg



CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username_password}@{host_ip_port}/tvbqnjbu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"



connect_db(app)

################################ Initial Request ##################################
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    """
    In Flask, g is a global object that is used to store data during the lifetime of a request. It is a simple way to store data that is specific to a single request and is accessible throughout the application.
    g stands for "context globals", which means that it is a container for variables that are shared within a specific context of the application. 
    In Flask, a context is defined as the lifetime of a request, which starts when a request is received and ends when a response is sent back to the client.
    """
    if CURR_USER_KEY in session:
        g.user = USER.query.get(session[CURR_USER_KEY])       
    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

################################### SIGN UP ##############################################################
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    active_page = 'signup'    
    if CURR_USER_KEY in session:
        return redirect("generate_qrcode")
    
    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data       
        email = form.email.data

        user = USER.signup( username, email , password)                                
           
        try:
            
            db.session.commit()
            do_login(user)

        except IntegrityError:
            flash("Username already taken . Please choose another username", 'danger')
            return render_template('users/signup.html', form=form)

        

        return redirect("generate_qrcode")

    else:
        return render_template('users/signup.html', form=form ,  active_page=active_page)

################################## HOMEPAGE ##############################################################
@app.route("/")
def root():
    """Homepage: redirect to homepage."""
    active_page = 'home'
    return render_template('home.html', active_page=active_page)

################################ LOGIN & LOGOUT ##########################################################
@app.route('/login' , methods=["GET", "POST"])
def login():
    if CURR_USER_KEY in session:
        return redirect("generate_qrcode")

    """Login Page"""
    active_page = 'login' 
    form = LoginForm()

    if form.validate_on_submit():
        user = USER.authenticate(form.username.data,
                                form.password.data)
        
        if user:
            do_login(user)
            flash(f"Welcome, {user.username}! . Please create your own QR code", "success")
            return redirect("/generate_qrcode")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form , active_page=active_page)

# LOGOUT
@app.route('/logout')
def logout():
    """Handle logout of user."""
    if CURR_USER_KEY not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    do_logout()
    flash("Goodbye!!!","success")
    return redirect('/')

############################### GENERATE QR CODE #########################################################
@app.route('/generate_qrcode', methods=['GET', 'POST'])
def generate_qrcode():
    if CURR_USER_KEY not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    
    form = QRCodeForm()

    if request.method == 'POST' and form.validate_on_submit():
        url = "https://qrcode3.p.rapidapi.com/qrcode/text"
        headers = {
            "Accept": "image/svg+xml",
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "0661f8c2acmsh9bdd2554608a245p19594fjsn7693a33cdc38",
            "X-RapidAPI-Host": "qrcode3.p.rapidapi.com"            
        }

        # image_url = url_for('static', filename='Logo.png', _external=True)

        data = {
            "data": form.data.data,
            "style": {
                "background": {
                "color": "#FFFFFF"
                },
                "module": {
                    "shape": form.module_shape.data,
                    "color": form.module_color.data
                },
                "inner_eye": {
                    "shape": form.inner_eye_shape.data,
                    "color": form.inner_eye_color.data
                },
                "outer_eye": {
                    "shape": form.outer_eye_shape.data,
                    "color": form.outer_eye_color.data
                }
            },
            "image": {
                "uri": "icon://bitcoin"
                # "url": form.image
            },
            "output": {
                "filename": "qrcode",
                "format": "png"
            },
            "size": {
                "width": 300,
                "quiet_zone": 4,
                "error_correction": "M"
            },
        }

        response = requests.post(url, json=data, headers=headers)
        
        if response.ok:  
            image_data = response.content           
            
            encoded_image = base64.b64encode(image_data).decode('utf-8') 
            
            # Open the image using PIL
            image = Image.open(BytesIO(image_data))

            # Adjust image quality and format
            image = image.convert("RGB")  # Convert to RGB for better quality

            # Create a BytesIO object to hold the modified image data
            modified_image_data = BytesIO()
            image.save(modified_image_data, format="JPEG", optimize=True)  # Save as JPEG with quality of 90%

            # Resize the image to a specific width and height
            image = image.resize((800, 600), resample=Image.LANCZOS)

            # Reset the BytesIO object's position to the beginning
            modified_image_data.seek(0)

            # # Read the modified image data as bytes
            encoded_image = base64.b64encode(modified_image_data.read()).decode('utf-8')
                    
            flash('QR code created','success')
            return render_template("users/showQRCode.html", image=encoded_image)
        else:
            flash("Error occurred during QR code generation",'danger')
            return redirect('/generate_qrcode')

    return render_template('users/createQRCodeForm.html', form=form)


################################### SAVE IMAGE TO DB ####################################################
# @app.route('/saveImage',methods=['POST'])
# def save_image():
#     if "user_id" not in session:
#         flash("Please login first!", "danger")
#         return redirect('/login')
    
#     user = g.user

#     form = ShowImageForm()

#     if form.validate_on_submit():
#        description = form.description.data

#        db.session.add(description)
#        db.session.commit()
#        flash('SAVE QR CODE to your collection list','success')
#        return redirect(f"/users/{user.id}")
     









if __name__ == '__main__':
    app.run()