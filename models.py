from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    country_code = db.Column(db.String(5), nullable=False)

    def __repr__(self) -> str:
        return f"User('{self.name}', '{self.email}', '{self.password}', '{self.number}', '{self.country_code}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(10), nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    order_type = db.Column(db.String(50), nullable=False)
    estimated_time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")

    def __repr__(self) -> str:
        return (
            f"Order('{self.admin_id}', '{self.customer_name}', '{self.customer_phone}', "
            f"'{self.product_name}', '{self.quantity}', '{self.price}', '{self.date}', "
            f"'{self.order_type}', '{self.estimated_time}', '{self.status}')"
        )