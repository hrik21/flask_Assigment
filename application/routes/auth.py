from flask import Blueprint,jsonify,request
from flask import Response
import application
from application.models.base_model import User,Contact
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
auth_bp = Blueprint("auth", __name__)
def data(value):
    details=[]
    for i in value:
        data_value={}
        data_value["name"]=i.name
        data_value['email']=i.email
        data_value['phone']=i.phone
        if type(value[0])==application.models.base_model.User:
            data_value['password']=i.password
        else:
            data_value['country']=i.country            
        data_value['address']=i.address
        details.append(data_value)
        return details
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
        abc=data(user)
        return jsonify({"data":abc})
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
        abc=data(contact)
        return jsonify({"data":abc})             
@auth_bp.route("/search",methods=['POST'])
def search_contacts():
    if request.method=='POST':
        data_=request.get_json()
        Data= Contact.query.filter((Contact.email ==data_["value"]) | (Contact.name == data_["value"]) | (Contact.phone == data_["value"]) ).all()
        if Data:
            abc=data(Data)
            return jsonify({"data":abc})
            
        else:
            return jsonify({"message":"contact does not exist"})   
@auth_bp.route('/show_contact',methods=['GET'])
@get_token
def show_contact(value):
    if request.method=='GET':
        contacts = Contact.query.filter_by(user_id=value['id']).all()
        abc=data(contacts)
        return jsonify({"data":abc})        
@auth_bp.route('/user_token',methods=['GET'])
@get_token
def user_token(value):
    if request.method=='GET':
        user = User.query.filter_by(id=value['id']).all()
        if user:
            abc=data(user)
        return jsonify({"data":abc})                     
