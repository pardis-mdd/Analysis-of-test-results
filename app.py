from myproject import app, db
from flask import render_template, redirect, request, url_for, flash, abort, session
from flask_login import login_user, login_required, logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm, ForgotPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from functools import wraps
from pdf_processor import extract_text_from_pdf, extract_values, analyze_results
from flask import Flask, render_template, request
import os
import tempfile
from werkzeug.utils import secure_filename
from pdf_processor2 import extract_text_from_pdf2, extract_values2, analyze_results2


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session or not session["email"]:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products")
@login_required
def products():
    return render_template("products.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("لطفاً همه فیلدها را پر کنید.", "error")
            return render_template("login.html")

        user = User.query.filter_by(email=email).first()

        if user:
            if user.check_password(password):
                session["email"] = user.email
                session["username"] = user.username
                return redirect(url_for("products"))
            else:
                flash("رمز عبور وارد شده اشتباه است. ", "error")
        else:
            flash("کاربر یافت نشد. لطفا ابتدا ثبت نام کنید.", "error")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("name2")
        email = request.form.get("email2")
        password = request.form.get("password2")

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if not username or not email or not password:
            flash("لطفاً تمامی فیلدها را پر کنید.", "error")
            return redirect(request.url)
        if existing_user:
            flash(
                "نام کاربری یا ایمیل قبلا استفاده شده است. لطفا یک مورد دیگر انتخاب کنید.",
                "error",
            )
            return redirect(request.url)

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("ثبت نام شما با موفقیت انجام شد! اکنون می‌توانید وارد شوید.", "success")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            flash("لطفا ایمیل خود را وارد کنید.", "error")
            return redirect(url_for("forgot_password"))
        user = User.query.filter_by(email=email).first()

        if user:
            flash(
                "یک ایمیل حاوی دستورالعمل‌های بازیابی رمز عبور به شما ارسال شده است.",
                "success",
            )
            return redirect(url_for("login"))
        else:
            flash("هیچ حساب کاربری با این آدرس ایمیل یافت نشد.", "error")
            return redirect(url_for("forgot_password"))

    return render_template("forget.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


def send_password_reset_email(user, token):
    subject = "Reset Your Password"
    recipient = user.email
    sender = "drai@gmail.com"
    reset_link = url_for("reset_password", token=token, _external=True)
    body = f"Hello {user.username},\n\nTo reset your password, please click on the following link:\n{reset_link}\n\nIf you did not request this, please ignore this email."

    # Send the email
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = body


@app.route("/blood_sugar_test", methods=["GET", "POST"])
def upload_blood_test():
    error = None
    success = None

    if request.method == "POST":
        if "file" not in request.files:
            error = "No file part"
        else:
            file = request.files["file"]
            if file.filename == "":
                error = "No selected file"
            elif not file.filename.endswith(".pdf"):
                error = "Please upload a PDF file."
            else:
                pdf_text = extract_text_from_pdf(file)
                blood_test_results = extract_values(pdf_text)
                analysis = analyze_results(blood_test_results)

                age = request.form.get("age")
                gender = request.form.get("gender")
                sickness = request.form.get("sickness")
                success = "File uploaded successfully and all fields filled."

                return render_template(
                    "results.html",
                    age=age,
                    gender=gender,
                    sickness=sickness,
                    blood_test_results=blood_test_results,
                    analysis=analysis,
                )

    return render_template("upload.html", error=error, success=success)


@app.route("/blood_test", methods=["GET", "POST"])
def upload_blood_sugar_test():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("upload.html", error="No file part")

        file = request.files["file"]
        if file.filename == "":
            return render_template("upload.html", error="No selected file")

        if file and file.filename.endswith(".pdf"):

            temp_pdf_path = os.path.join(
                tempfile.gettempdir(), secure_filename(file.filename)
            )
            file.save(temp_pdf_path)

            pdf_text = extract_text_from_pdf2(temp_pdf_path)
            blood_test_results = extract_values2(pdf_text)
            analysis = analyze_results2(blood_test_results)

            age = request.form.get("age")
            gender = request.form.get("gender")
            sickness = request.form.get("sickness")

            os.remove(temp_pdf_path)

            return render_template(
                "results.html",
                age=age,
                gender=gender,
                sickness=sickness,
                blood_test_results=blood_test_results,
                analysis=analysis,
            )
        else:
            return render_template("upload.html", error="Please upload a PDF file.")

    return render_template("upload.html")


@app.route("/upload")
@login_required
def upload():
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
