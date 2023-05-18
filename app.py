import requests
from flask import Flask, redirect, render_template , flash , g , session , request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, USER 
from forms import QRCodeForm , SignUpForm , LoginForm
from sqlalchemy.exc import IntegrityError
from secret import username_password , host_ip_port

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username_password}@{host_ip_port}/tvbqnjbu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

connect_db(app)

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


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = USER.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data                
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)



@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/login")


@app.route('/login' , methods=["GET", "POST"])
def login():
    """Login Page"""
    form = LoginForm()

    if form.validate_on_submit():
        user = USER.authenticate(form.username.data,
                                 form.password.data)
        
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return render_template("users/secret.html")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)













    return render_template('login.html')


@app.route('/generate_qrcode', methods=['GET', 'POST'])
def generate_qrcode():
    form = QRCodeForm()

    if request.method == 'POST' and form.validate_on_submit():
        url = "https://qrcode-monkey.p.rapidapi.com/qr/custom"
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
            "Content-Type": "application/json"
        }

        data = {
            'data': form.data.data,
            'config': {
                'body': form.body.data,
                'logo': form.logo.data
            },
            'size': form.size.data,
            'download': form.download.data,
            'file': form.file.data
        }

        response = requests.post(url, json=data, headers=headers)
        if response.ok:
            return jsonify(response.json())
        else:
            return jsonify({"message": "Error occurred during QR code generation"})

    return render_template('generate_qrcode.html', form=form)


if __name__ == '__main__':
    app.run()