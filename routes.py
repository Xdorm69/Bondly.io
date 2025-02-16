from flask import redirect, render_template, request, session
from otp import send_otp
from models import User
import random

def register_routes(app, db):
    @app.route("/")
    def landing():
        return render_template("landing.html")

    @app.route("/maintainence")
    def maintainence():
        return render_template("maintainence.html")

    @app.route("/signin", methods=["GET", "POST"])
    def signin():
        msg = None
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            if not all([email, password]):
                msg = "Please fill all the fields"
                print(msg)
            elif User.query.filter_by(email=email, password=password).first():
                session["email"] = email
                session["name"] = User.query.filter_by(email=email).first_or_404().name
                return render_template("success.html", return_msg="Your account has been logged in successfully", link="/dashboard")
            else:
                msg = "Invalid email or password"
                print(msg)

        return render_template("signin.html", link="signup", msg=msg)

    @app.route("/success")
    def success():
        return render_template("success.html", return_msg="", link="/signin")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        msg = None
        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            confirm_password = request.form["confirm_password"]
            password = request.form["password"]
            number = request.form["number"]
            country_code = request.form["country_code"]

            if not all([name, email, password, number, country_code]):
                msg = "Please fill all the fields"
            elif password != confirm_password:
                msg = "Passwords do not match"
                print(msg)
            elif len(password) < 8:
                msg = "Password must be at least 8 characters"
                print(msg)
            elif len(number) != 10:
                msg = "Number must be at least 10 characters"
                print(msg)
            elif User.query.filter_by(email=email).first():
                msg = "Email already exists"
                print(msg)
            elif User.query.filter_by(number=number).first():
                msg = "Number already exists"
                print(msg)
            else:
                msg = None
                print("Signup successful")
                db.session.add(User(name=name, email=email, password=password, number=number, country_code=country_code))
                db.session.commit()
                return render_template("success.html", return_msg="Your account has been created successfully", link="/signin")

        return render_template("signup.html" , link="signin", msg=msg)
    
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/signin")
    
    @app.route("/otp", methods=["GET", "POST"])
    def otp():
        msg = None
        color = "red"

        if request.method == "POST":
            otp = request.form.get("otp")
            if not otp:
                msg = "Please enter your otp"
                print(msg)
            elif otp == str(session.get("otp")):
                return render_template("changepass.html", msg= "OTP verified", color="green")
            else:
                msg = "Invalid otp"
                print(msg)
        return render_template("otp.html", msg=msg, color="red")
    
    @app.route("/resendotp")
    def resendotp():
        otp = random.randint(100000, 999999)
        session["otp"] = otp
        send_otp(session.get("email"), otp)
        return redirect("/otp")
    
    @app.route("/forgotpassword", methods=["GET", "POST"])
    def forgetpassword():
        msg = None
        if request.method == "POST":
            email = request.form.get("email")
            session["email"] = email
            session["password"] = User.query.filter_by(email=email).first_or_404().password
            if not email:
                msg = "Please enter your email"
                print(msg)
            elif User.query.filter_by(email=email).first():
                otp = random.randint(100000, 999999)
                session["otp"] = otp
                send_otp(email, otp)
                return redirect("/otp")
            else:
                msg = "Email does not exist"
                print(msg)
        return render_template("forgotpassword.html", msg=msg) 
    
    @app.route("/changepassword", methods=["GET", "POST"])
    def changepassword():
        msg = None
        color = "red"
        if request.method == "POST":
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            if not all([password, confirm_password]):
                msg = "Please enter your password"
                print(msg)
            elif password != confirm_password:
                msg = "Passwords do not match"
                print(msg)
            elif session.get("password") == password:
                msg = "New password cannot be the same as the old password"
                print(msg)
                color = "red"
            elif len(password) < 8:
                msg = "Password must be at least 8 characters"
                print(msg)
            else:
                user = User.query.filter_by(email=session.get("email")).first()
                user.password = password
                db.session.commit()
                session.clear()
                return render_template("success.html", return_msg="Your password has been changed successfully", link="/signin")
        return render_template("changepass.html", msg=msg, color=color)

    # PROTECTED ROUTES 

    @app.route("/dashboard")
    def dashboard():
        if not session.get("email"):
            return render_template("signin.html" , msg="Please login to access dashboard")
        return render_template("dashboard.html", name=session.get("name"))  

    @app.errorhandler(404)
    def not_found(e):
        return render_template("maintainence.html")

    @app.route("/dashboard/top-employees")
    def top_employees():
        if not session.get("email"):
            return render_template("signin.html" , msg="Please login to access dashboard")
        return render_template("top-employees.html")