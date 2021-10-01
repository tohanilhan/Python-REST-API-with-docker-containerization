import pymongo
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from bson.json_util import ObjectId
from bson.json_util import dumps

# Making a Connection with MongoClient
client = MongoClient("mongodb://my_db:27017")
# database
db = client["ProductManagementDB"]
# collection
user = db["UserInfo"]

app = Flask(__name__)
jwt = JWTManager(app)

# JWT Config
app.config["JWT_SECRET_KEY"] = "tohan_is_the_secretkey"

# İnitializing Database For the first time
user_info = dict(Name="Atahan", Surname="Ilhan", Email="atahanilhan@gmail.com", Password="atahan")
test=user.find_one(user_info)
if not test:
    user.insert_one(user_info)
user_info2 = dict(Name="Burak", Surname="Gulbay", Email="burak.gulbay@deepcase.com.tr", Password="burak")
test2=user.find_one(user_info2)
if not test2:
    user.insert_one(user_info2)

product_info = dict(Name="Hyperx Cloud Flight Wireless Headset", Price="$140", Quantity="98")
test3=db.ProductInfo.find_one(product_info)
if not test3:
    db.ProductInfo.insert_one(product_info)
product_info2 = dict(Name="Razer Ornata Chroma Keyboard", Price="$130", Quantity="160")
test4=db.ProductInfo.find_one(product_info2)
if not test4:
    db.ProductInfo.insert_one(product_info2)

# Login
@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        auth_email = request.json["Email"]
        auth_password = request.json["Password"]
    else:
        auth_email = request.form["Email"]
        auth_password = request.form["Password"]

    
    test = user.find_one({"Email": auth_email, "Password": auth_password})
    
    if test:
        token = create_access_token(identity=auth_email)
        return jsonify(message="Login Succeeded!", access_token=token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401

# To see all users
@app.route("/users", methods=["GET"])
@jwt_required()
def allusers():
    users=user.find()
    respond=dumps(users)
    return respond

# To see a specific user
@app.route('/users/<id>')
@jwt_required()
def oneuser(id):
    one_user=user.find_one({'_id':ObjectId(id)})
    respond=dumps(one_user)
    return respond

# To register a new user
@app.route("/register", methods=["POST"])
@jwt_required()
def register():
    email = request.form["Email"]
    test = user.find_one({"Email": email})
    if test:
        return jsonify(message="User Already Exist"), 409
    else:
        name = request.form["Name"]
        surname = request.form["Surname"]
        password = request.form["Password"]

        user_info = dict(Name=name, Surname=surname, Email=email, Password=password)
        user.insert_one(user_info)

        return jsonify(message="User added sucessfully"), 201

# To update a specific user
@app.route('/updateuser/<id>', methods=["PUT"])
@jwt_required()
def update_user(id):

    _id=id
    form=request.form
    name=form['Name']
    surname=form['Surname']
    email=form['Email']
    password=form['Password']

    if name and email and password and _id and request.method =='PUT': 
        
        user.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'Name':name,'Surname':surname,'Email':email,'Password':password}})
        return jsonify(message='User updated successfully '),200

    else:
        return not_found()

# To delete a specific user
@app.route('/deleteuser/<id>', methods=["DELETE"])
@jwt_required()
def delete_user(id):
    
    find = user.find_one({"_id": ObjectId(id)})
    if find:
        user.delete_one({"_id":ObjectId(id)})
        return jsonify(message="User deleted Successfully"), 201
    else:
        return jsonify(message="User cannot found"), 404

# To see all products
@app.route('/products', methods=["GET"])
@jwt_required()
def products():
    products = db.ProductInfo.find()
    resp=dumps(products)
    return resp

# To see specific product 
@app.route('/products/<id>')
@jwt_required()
def product(id):
    one_product=db.ProductInfo.find_one({'_id':ObjectId(id)})
    respond=dumps(one_product)
    return respond

# To add a new product
@app.route("/addproduct",methods=['POST'])
@jwt_required()
def add_product():
    
    name=request.form['Product Name']
    price=request.form['Price']
    quantity=request.form['Quantity']
    

    if name and price and quantity and request.method == 'POST':
        
        db.ProductInfo.insert({'Product Name':name, 'Price':price,'Quantity':quantity})

        return jsonify(message="Product added successfully"), 200

    else:

        return not_found()

# To update a specific product
@app.route('/updateproduct/<id>', methods=["PUT"])
@jwt_required()
def update_product(id):

    _id=id
    
    name=request.form['Product Name']
    price=request.form['Price']
    quantity=request.form['Quantity']
    

    if name and price and quantity and _id and request.method =='PUT': 
        
        db.ProductInfo.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'Product Name':name,'Price':quantity,'Price':price}})
       
        return jsonify(message="Product updated successfully "), 200

    else:
        return not_found()

# To delete a specific product
@app.route('/deleteproduct/<id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):

    db.ProductInfo.delete_one({'_id':ObjectId(id)})
    resp = jsonify("Product deleted successfully ")
    resp.status_code=200

    return resp

# To handle Not Found Error
@app.errorhandler(404)
def not_found(error=None):
    message ={
        'status':404,
        'message':'Not Found ' + request.url
    }

    resp=jsonify(message)

    resp.status_code=404
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)