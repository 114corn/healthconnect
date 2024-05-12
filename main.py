from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return abort(401, description="Bad username or password")

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return abort(400, description="User already exists")
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/patients', methods=['POST'])
@jwt_required()
def add_patient():
    data = request.get_json()
    new_patient = Patient(name=data['name'], dob=data['dob'])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully'}), 201

@app.route('/patients/<int:id>', methods=['GET'])
@jwt_required()
def get_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    if not patient:
        return abort(404, description="Patient not found")
    return jsonify({ 'name': patient.name, 'dob': patient.dob }), 200

@app.route('/appointments', methods=['POST'])
@jwt_required()
def schedule_appointment():
    data = request.get_json()
    new_appointment = Appointment(patient_id=data['patient_id'], date=data['date'], description=data['description'])
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment scheduled successfully'}), 201

@app.route('/appointments/<int:id>', methods=['GET'])
@jwt_required()
def get_appointment(id):
    appointment = Appointment.query.filter_by(id=id).first()
    if not appointment:
        return abort(404, description="Appointment not found")
    return jsonify({ 'patient_id': appointment.patient_id, 'date': appointment.date, 'description': appointment.description }), 200

if __name__ == '__main__':
    app.run(debug=True)