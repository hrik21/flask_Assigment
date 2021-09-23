from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(200))
    phone=db.Column(db.BigInteger)
    email=db.Column(db.String(200),unique=True)
    address=db.Column(db.String(1000),unique=True)
    password = db.Column(db.String(100))
    contact = db.relationship('Contact', backref='user',lazy=True)
class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(200))
    phone=db.Column(db.BigInteger)
    email=db.Column(db.String(200))
    address=db.Column(db.String(1000),unique=True)
    country=db.Column(db.String(200))
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))