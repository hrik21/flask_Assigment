from flask import Blueprint,jsonify,request
from flask import Response
from application.models.base_model import User,Contact
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
auth_bp = Blueprint("auth", __name__)

def get_token(f):
    @wraps(f)
    def decorated():
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
            value=jwt.decode(token,"secret",algorithms=["HS256"])
            return f(value)
        if not token:
            return jsonify({"message":"token missing"}),401    
    return decorated
@auth_bp.route('/signup',methods=['POST'])
def signup():
    if request.method=='POST':
        data=request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({"messgae":"user already exist"})
           
        else:
            new_user = User(email=data["email"], name=data["name"], password=generate_password_hash(data["password"], method='sha256'),phone=data["phone"],address=data["address"])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message":"user created"})
@auth_bp.route("/login")
def login():
    auth=request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "invalid credential"})
    user=User.query.filter_by(email=auth.username).first()  
    if not user:
        return jsonify({"message": "invalid credential"})
    if check_password_hash(user.password,auth.password):
        token=jwt.encode({'id':user.id},"secret", algorithm="HS256")
        
        return jsonify({"token":token})
    else:
       return jsonify({"message": "invalid credential"})     
@auth_bp.route("/user",methods=['GET'])
def user_details():
    if request.method=='GET':
        user=User.query.all()
        details=[]
        for i in user:
            data_user={}
            data_user['name']=i.name
            data_user['email']=i.email
            data_user['phone']=i.phone
            data_user['password']=i.password
            data_user['address']=i.address
            details.append(data_user)
        return jsonify({"data":details})
@auth_bp.route('/contact',methods=['POST'])
@get_token
def new_contact(value):
    if request.method=='POST':
        data=request.get_json()
        contact = Contact.query.filter_by(email=data['email']).first()
        if contact:
            return jsonify({"messgae":"Contact already exist"})
           
        else:
            new_contact = Contact(user_id=value["id"],email=data["email"], name=data["name"], country=data["country"] ,phone=data["phone"],address=data["address"])
            db.session.add(new_contact)
            db.session.commit()
            return jsonify({"message":"Contact created"})                      
@auth_bp.route("/show",methods=['GET'])
def show_contacts():
    if request.method=='GET':
        contact=Contact.query.all()
        details=[]
        for i in contact:
            data_contact={}
            data_contact['name']=i.name
            data_contact['email']=i.email
            data_contact['phone']=i.phone
            data_contact['country']=i.country
            data_contact['address']=i.address
            details.append(data_contact)
        return jsonify({"data":details})             
@auth_bp.route("/search",methods=['POST'])
def search_contacts():
    if request.method=='POST':
        data=request.get_json()
        data= Contact.query.filter((Contact.email ==data["value"]) | (Contact.name == data["value"]) | (Contact.phone == data["value"]) ).first()
        if data:
            data_contact={}
            data_contact['name']=data.name
            data_contact['email']=data.email
            data_contact['phone']=data.phone
            data_contact['country']=data.country
            data_contact['address']=data.address
            return jsonify({"data":data_contact})
            
        else:
            return jsonify({"message":"contact does not exist"})            