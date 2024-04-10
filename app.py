from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort,session
from flask_login import login_user,login_required,logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm,ForgotPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or not session['email']:  # Check if 'email' is not in session or if it's empty
            return redirect(url_for('login'))  # Redirect to the login page if user is not logged in
        return f(*args, **kwargs)
    return decorated_function
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
@login_required
def products():
    return render_template('products.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if user.check_password(password):
                session['email'] = user.email
                return redirect('/products')
            else:
                flash('Invalid password. Please try again.', 'error')
        else:
            flash('User not found. Please register.', 'error')

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('name2')
        email = request.form.get('email2')
        password = request.form.get('password2')

        # Check if the username or email is already in use
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if not username or not email or not password:
            flash('All fields are required. Please fill in all the fields.', 'error')
            return redirect(request.url)  # Redirect back to the registration page
        if existing_user:
            flash('Username or email is already in use. Please choose another.', 'error')
            return redirect(request.url)  # Redirect back to the registration page
        
       

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect('/login')

    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:  # Check if email is empty
            flash('Please provide an email address.', 'error')
            return redirect(url_for('forgot_password'))
        user = User.query.filter_by(email=email).first()
  
        
        if user:
            # Generate a token and send the password reset email
            
            flash('An email has been sent with instructions to reset your password.')
            return redirect(url_for('login'))  # Assuming 'login' is the route for the login page
        else:
            flash('No account found with that email address.', 'error')  # 'error' could be a CSS class for displaying error messages
            # Don't redirect here, keep the user on the same page
            # Returning the template directly will render the page with the flash message
            return redirect(url_for('forgot_password'))

    return render_template('forget.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def send_password_reset_email(user, token):
    # Compose the email message
    subject = "Reset Your Password"
    recipient = user.email
    sender = "your_email@example.com"  # Adjust this to your email address
    reset_link = url_for('reset_password', token=token, _external=True)  # Assuming 'reset_password' is the route for password reset
    body = f"Hello {user.username},\n\nTo reset your password, please click on the following link:\n{reset_link}\n\nIf you did not request this, please ignore this email."

    # Send the email
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = body

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')  

if __name__ == '__main__':
    app.run(debug=True)