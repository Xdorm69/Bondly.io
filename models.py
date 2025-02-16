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
