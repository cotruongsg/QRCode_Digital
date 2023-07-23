import requests
from flask import Flask, redirect, render_template , flash , g , session , request , url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, USER ,  QRC_IMAGES_DB
from forms import QRCodeForm , SignUpForm , LoginForm 
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from secret import username_password , host_ip_port
import base64
from io import BytesIO
from PIL import Image




CURR_USER_KEY = "curr_user"

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username_password}@{host_ip_port}/tvbqnjbu'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username_password}@{host_ip_port}/qr'
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

        

        return redirect(f"/users/{user.id}/collections")

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
        return redirect(f"/users/{g.user.id}/collections")

    """Login Page"""
    active_page = 'login' 
    form = LoginForm()

    if form.validate_on_submit():
        user = USER.authenticate(form.username.data,
                                form.password.data)       
        
        if user:
            do_login(user)
            flash(f"Welcome, {user.username}! . Please create your own QR code", "success")
            return redirect(f"/users/{user.id}/collections")

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


############################### SHOW QR CODE COLLECTION LIST ###############################################
# SHOW EXISTING COLLECTION LIST
@app.route('/users/<int:user_id>/collections')
def show_all_qrCodeCollections(user_id):
    if CURR_USER_KEY not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    user = USER.query.get_or_404(user_id)
    
    """Return a list of collection."""
    if session[CURR_USER_KEY] != user.id:
        flash("Access unauthorized to another user. Please login your username", "danger")
        return redirect("/login")
    
    images = QRC_IMAGES_DB.query.filter_by(user_id=user_id).all()
    image_ids = QRC_IMAGES_DB.query.filter_by(user_id=user_id).with_entities(QRC_IMAGES_DB.id).all()

       
    if images:
        image_data_list = []
        for image in images:
            image_data = base64.b64encode(image.image).decode('utf-8')
            qrCodeImage = {
                'name': image.name,
                'description': image.description,
                'image_data': image_data
            }
            image_data_list.append(qrCodeImage)     
        
        return render_template("users/showQRCodeCollections.html", user=user, qrCodeImagesTB=image_data_list , image_id=image_ids)
    
    return render_template("users/showQRCodeCollections.html", user=user)


############################### GENERATE QR CODE #########################################################
@app.route('/users/<int:user_id>/generate_qrcode', methods=['GET', 'POST'])
def generate_qrcode(user_id):
    if CURR_USER_KEY not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    user = USER.query.get_or_404(user_id)

    if user:
        if session.get(CURR_USER_KEY) != user.id:
            flash("Access unauthorized to another user. Please log in with your username.", "danger")
            return redirect(f"/users/{g.user.id}/generate_qrcode")
      
    form = QRCodeForm()

    if request.method == 'POST' and form.validate_on_submit():
        url = "https://qrcode3.p.rapidapi.com/qrcode/text"
        headers = {
            "Accept": "image/svg+xml",
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "3df2b6ddb8mshd7c4ae3a0e60575p16bcbajsn226b72e66935",
            "X-RapidAPI-Host": "qrcode3.p.rapidapi.com"            
        }

        qrname = form.name.data;
        qrdescriptions = form.description.data;
        module_shape = form.module_shape.data;
        module_color = form.module_color.data;
        inner_eye_shape = form.inner_eye_shape.data;
        inner_eye_color = form.inner_eye_color.data;
        outer_eye_shape = form.outer_eye_shape.data;
        outer_eye_color = form.outer_eye_color.data;
        your_url = form.data.data;

        data = {
            "data": your_url,
            "style": {
                "background": {
                "color": "#FFFFFF"
                },
                "module": {
                    "shape": module_shape,
                    "color": module_color
                },
                "inner_eye": {
                    "shape": inner_eye_shape,
                    "color": inner_eye_color
                },
                "outer_eye": {
                    "shape": outer_eye_shape,
                    "color": outer_eye_color
                }
            },
            # "image": {
            #     "uri": "icon://heart"                
            # },
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
        print(response)
        
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

            # Read the modified image data as bytes
            encoded_image = base64.b64encode(modified_image_data.read()).decode('utf-8')
           
            # Save the QR code image to the database
            qr_code_image = QRC_IMAGES_DB(
                name = qrname,
                description = qrdescriptions,
                web_url = your_url,
                module_shape = module_shape,
                module_color = module_color,
                inner_eye_shape = inner_eye_shape,
                inner_eye_color = inner_eye_color,
                outer_eye_shape = outer_eye_shape,
                outer_eye_color = outer_eye_color,
                image = base64.b64decode(encoded_image),
                user_id = user.id
            )
            db.session.add(qr_code_image)
            db.session.commit()

            flash('QR code created','success')          
           
            return redirect(url_for('show_user_qrcode', user_id=user.id))
        else:
            flash("Error occurred during QR code generation . Please try again",'danger')
            return redirect(f'/users/<int:user_id>/generate_qrcode')

    return render_template('users/createQRCodeForm.html', form=form)


########################################### Show QR Code ####################################################
@app.route('/users/<int:user_id>/qrcode', methods=['GET'])
def show_user_qrcode(user_id):
    if CURR_USER_KEY not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    user = USER.query.get_or_404(user_id)

    if user:
        if session.get(CURR_USER_KEY) != user.id:
            flash("Access unauthorized to another user. Please log in with your username.", "danger")
            return redirect(f"/users/{g.user.id}/qrcode")

    latest_image = QRC_IMAGES_DB.query.filter_by(user_id=user_id).order_by(QRC_IMAGES_DB.id.desc()).first()

    if not latest_image:        
        # Handle the case where the image data is not available
        flash("QR code image not found", "danger")
        return redirect(url_for('generate_qrcode', user_id=user_id))
    
    get_image = latest_image.image
    image = base64.b64encode(get_image).decode('utf-8')
    
    return render_template("users/showQRCode.html", image=image , user=user)


########################################### DELETE QR Code ####################################################
@app.route('/users/<int:user_id>/collections/delete/<int:image_id>', methods=['POST'])
def delete_qrCodeCollection(user_id, image_id):
    if CURR_USER_KEY not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    user = USER.query.get_or_404(user_id)

    """Delete the specified collection."""
    if session[CURR_USER_KEY] != user.id:
        flash("Access unauthorized to another user. Please login with your username.", "danger")
        return redirect("/login")

    # Retrieve the image by user_id and image_id
    image = QRC_IMAGES_DB.query.filter_by(user_id=user_id, id=image_id).first()

    if image:
        # Delete the image from the database
        db.session.delete(image)
        db.session.commit()
        flash("Image deleted successfully.", "success")
    else:
        flash("Image not found.", "danger")

    return redirect(f"/users/{user_id}/collections")


########################################### EDIT QR Code ####################################################
@app.route('/users/<int:user_id>/collections/edit/<int:image_id>', methods=['GET', 'POST'])
def edit_qrCodeCollection(user_id, image_id):
    if CURR_USER_KEY not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    user = USER.query.get_or_404(user_id)

    """Edit the specified collection."""
    if session[CURR_USER_KEY] != user.id:
        flash("Access unauthorized to another user. Please login with your username.", "danger")
        return redirect("/lo6gin")

    # Retrieve the image by user_id and image_id
    edit_image = QRC_IMAGES_DB.query.filter_by(user_id=user_id, id=image_id).first()

    if not edit_image:
        flash("Image not found.", "danger")
        return redirect(f"/users/{user_id}/collections")

    form = QRCodeForm()

    if request.method == 'POST' and form.validate_on_submit():
        url = "https://qrcode3.p.rapidapi.com/qrcode/text"
        headers = {
            "Accept": "image/svg+xml",
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "3df2b6ddb8mshd7c4ae3a0e60575p16bcbajsn226b72e66935",
            "X-RapidAPI-Host": "qrcode3.p.rapidapi.com"            
        }

        qrname = form.name.data;
        qrdescriptions = form.description.data;
        module_shape = form.module_shape.data;
        module_color = form.module_color.data;
        inner_eye_shape = form.inner_eye_shape.data;
        inner_eye_color = form.inner_eye_color.data;
        outer_eye_shape = form.outer_eye_shape.data;
        outer_eye_color = form.outer_eye_color.data;
        your_url = form.data.data;       

        data = {
            "data": your_url,
            "style": {
                "background": {
                "color": "#FFFFFF"
                },
                "module": {
                    "shape": module_shape,
                    "color": module_color
                },
                "inner_eye": {
                    "shape": inner_eye_shape,
                    "color": inner_eye_color
                },
                "outer_eye": {
                    "shape": outer_eye_shape,
                    "color": outer_eye_color
                }
            },
            # "image": {
            #     "uri": "icon://heart"                
            # },
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

            # Read the modified image data as bytes
            encoded_image = base64.b64encode(modified_image_data.read()).decode('utf-8')

            # Update the image properties
            edit_image.name = qrname;
            edit_image.description = qrdescriptions
            edit_image.web_url = your_url
            edit_image.module_shape = module_shape
            edit_image.module_color = module_color
            edit_image.inner_eye_shape = inner_eye_shape
            edit_image.inner_eye_color = inner_eye_color
            edit_image.outer_eye_shape = outer_eye_shape
            edit_image.outer_eye_color = outer_eye_color
            edit_image.image = base64.b64decode(encoded_image)

            db.session.commit()

            flash("Image updated successfully.", "success")
            return redirect(f"/users/{user_id}/collections")

    # Pre-populate the form fields with the current image data
    form.name.data = edit_image.name
    form.description.data = edit_image.description
    form.data.data = edit_image.web_url
    form.module_shape.data = edit_image.module_shape
    form.module_color.data = edit_image.module_color
    form.inner_eye_shape.data = edit_image.inner_eye_shape
    form.inner_eye_color.data = edit_image.inner_eye_color
    form.outer_eye_shape.data = edit_image.outer_eye_shape
    form.outer_eye_color.data = edit_image.outer_eye_color


    return render_template('users/editQRCodeForm.html', form=form, user=user, image=edit_image)






if __name__ == '__main__':
    app.run()