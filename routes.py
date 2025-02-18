from flask import redirect, render_template, request, session
from otp import send_otp
from models import User
from models import Order
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
                session["id"] = User.query.filter_by(email=email).first().id
                session["email"] = email
                session["name"] = User.query.filter_by(email=email).first().name
                return render_template(
                    "success.html",
                    return_msg="Your account has been logged in successfully",
                    link="/dashboard",
                )
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
                db.session.add(
                    User(
                        name=name,
                        email=email,
                        password=password,
                        number=number,
                        country_code=country_code,
                    )
                )
                db.session.commit()
                return render_template(
                    "success.html",
                    return_msg="Your account has been created successfully",
                    link="/signin",
                )

        return render_template("signup.html", link="signin", msg=msg)

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
                return render_template(
                    "changepass.html", msg="OTP verified", color="green"
                )
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
            session["password"] = (
                User.query.filter_by(email=email).first_or_404().password
            )
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
                return render_template(
                    "success.html",
                    return_msg="Your password has been changed successfully",
                    link="/signin",
                )
        return render_template("changepass.html", msg=msg, color=color)

    # PROTECTED ROUTES

    @app.route("/dashboard")
    def dashboard():
        if not session.get("email"):
            return render_template(
                "signin.html", msg="Please login to access dashboard"
            )
        return render_template("dashboard.html", name=session.get("name"))

    @app.errorhandler(404)
    def not_found(e):
        if not session.get("email"):
            return render_template("maintainence.html")
        else:
            return "Page not found", 404

    @app.route("/dashboard/top-employees")
    def top_employees():
        if not session.get("email"):
            return render_template(
                "signin.html", msg="Please login to access dashboard"
            )
        return render_template("top-employees.html")

    @app.route("/dashboard/addorders", methods=["GET", "POST"])
    def add_order():
        if not session.get("email"):
            return render_template(
                "signin.html", msg="Please login to access dashboard"
            )
        return render_template("add-orders.html")

    @app.route("/orders")
    def orders():
        if not session.get("email"):
            return render_template(
                "signin.html", msg="Please login to access dashboard"
            )
        return render_template("orders.html")

    @app.route("/dashboard/customers")
    def customers():
        if not session.get("email"):
            return render_template(
                "signin.html", msg="Please login to access dashboard"
            )
        return render_template("customers.html")

    @app.route("/dashboard/best-items")
    def best_items():
        if not session.get("email"):
            return render_template(
                "signin.html", msg="Please login to access dashboard"
            )
        return render_template("best-items.html")

    @app.route("/addorders", methods=["GET", "POST"])
    def add_orders():
        if not session.get("email"):
            return render_template(
                "signin.html", msg="Please login to access dashboard"
            )
        print("Session Email: ", session.get("email"))
        if request.method == "POST":
            msg = None
            try:
                admin_id = session.get("id")
                customer_name = request.form.get("customer_name")
                customer_phone = request.form.get("customer_phone")
                product_name = request.form.get("product_name")
                quantity = request.form.get("quantity")
                price = request.form.get("price")
                date = request.form.get("date")
                order_type = request.form.get("order_type")
                estimated_time = request.form.get("estimated_time")
                status = "Pending"
                print(
                    f"Admin ID: {admin_id}, Customer Name: {customer_name}, Phone: {customer_phone}, Product: {product_name}, Quantity: {quantity}, Price: {price}, Date: {date}, Order Type: {order_type}, Estimated Time: {estimated_time}"
                )
                if not all(
                    [
                        admin_id,
                        customer_name,
                        customer_phone,
                        product_name,
                        quantity,
                        price,
                        date,
                        order_type,
                        estimated_time,
                    ]
                ):
                    msg = ("Please fill all the fields")
                    raise Exception("Please fill all the fields")
                if len(customer_phone) != 10:
                    msg = "Phone number should be of 10 digits"
                    raise Exception("Phone number should be of 10 digits")
                if not customer_phone.isdigit():
                    msg = "Phone number should contain only digits"
                    raise Exception("Phone number should contain only digits")
                if int(quantity) <= 0:
                    msg = "Quantity should be greater than 0"
                    raise Exception("Quantity should be greater than 0")
                if float(price) <= 0:
                    msg = "Price should be greater than 0"
                    raise Exception("Price should be greater than 0")
                order = Order(
                    admin_id=admin_id,
                    customer_name=customer_name,
                    customer_phone=customer_phone,
                    product_name=product_name,
                    quantity=quantity,
                    price=price,
                    date=date,
                    order_type=order_type,
                    estimated_time=estimated_time,
                    status=status,
                )
                db.session.add(order)
                db.session.commit()
                print("Order added successfully")
                return render_template(
                    "success.html",
                    return_msg="Order added successfully",
                    link="/dashboard/addorders",
                )
            except Exception as e:
                print(f"Error: {e}")
                return render_template("add-orders.html", msg=msg)
        print("GET")
        return render_template("add-orders.html")
