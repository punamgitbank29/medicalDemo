from flask import Flask,jsonify, request, render_template, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import config
import datetime
from src.database import get_user_collection
from src.utils import MedicalInsurance
Obj = MedicalInsurance()
user_collection = get_user_collection()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = 'secret-key'
jwt = JWTManager(app)

@app.route("/")
def landing():
    return render_template("login.html")

@app.route("/login-page")
def login_page():
    # Optional: keep this, or remove it
    return render_template("login.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/register", methods = ["POST"])
def user_registration():
    user_data = request.form
    user_name = user_data['user_name']
    password = user_data['password']
    email_id = user_data['email_id']
    contact_number = user_data['contact_number']
    dob = user_data['dob']
    
    response = user_collection.find_one({"email_id":email_id, "contact_number":contact_number})
    if not response:
        user_collection.insert_one({"email_id":email_id, "contact_number":contact_number, "user_name":user_name,
                                    "password":password, "dob":dob })
        print("User registered successfully")
        return jsonify({"message": "User registered successfully"})
    else:
        print("User Already Exists")
        return jsonify({"message": "User Already Exists"})

@app.route("/login", methods = ["POST"])
def user_login():
    user_data = request.form
    user_name = user_data['user_name']
    password = user_data['password']
    response = user_collection.find_one({"user_name":user_name, "password":password})
    if response:
        access_token = create_access_token(identity=user_name, expires_delta=datetime.timedelta(minutes=10))
        return jsonify({"status":"success", "message":"Login Successful", "token": access_token})
    else:
        return jsonify({"status":"failure", "message":"Invalid Credentials"})

@app.route("/gender_options")
@jwt_required()
def gender_options():
    col_data = Obj.load_json_data()
    gender_values = list(col_data['gender'].keys())
    return jsonify(gender_values)

@app.route("/region_options")
@jwt_required()
def region_options():
    model = Obj.load_model()
    print(model.feature_names_in_)
    region_values = [col.replace("region_","") for col in model.feature_names_in_ if "region_" in col]
    return jsonify(region_values)

@app.route("/prediction", methods = ["POST"])
@jwt_required()
def prediction():
    data = request.form
    print("data :", data)
    
    predicted_charges = Obj.predict_charges(data)

    return {"result": f"Predicted Medical insurance charges is: {predicted_charges}"}

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = config.FLASK_PORT_NUMBER, debug=True)
