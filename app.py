from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/railway_db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False)

# Endpoints
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']
    if role not in ['admin', 'user']:
        return jsonify({'msg': 'Invalid role'}), 400
    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify({'access_token': access_token}), 200
    return jsonify({'msg': 'Invalid credentials'}), 401

@app.route('/admin/train', methods=['POST'])
@jwt_required()
def add_train():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'msg': 'Access forbidden'}), 403
    data = request.get_json()
    train = Train(source=data['source'], destination=data['destination'], total_seats=data['total_seats'], available_seats=data['total_seats'])
    db.session.add(train)
    db.session.commit()
    return jsonify({'msg': 'Train added successfully'}), 201

@app.route('/availability', methods=['GET'])
def get_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')
    trains = Train.query.filter_by(source=source, destination=destination).all()
    result = [{'id': t.id, 'source': t.source, 'destination': t.destination, 'available_seats': t.available_seats} for t in trains]
    return jsonify(result), 200

@app.route('/book', methods=['POST'])
@jwt_required()
def book_seat():
    current_user = get_jwt_identity()
    data = request.get_json()
    train_id = data['train_id']
    seats = data['seats']
    train = Train.query.get(train_id)
    if train and train.available_seats >= seats:
        train.available_seats -= seats
        db.session.add(Booking(user_id=current_user['id'], train_id=train_id, seats_booked=seats))
        db.session.commit()
        return jsonify({'msg': 'Booking successful'}), 200
    return jsonify({'msg': 'Not enough seats available'}), 400

@app.route('/booking/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking_details(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        return jsonify({'user_id': booking.user_id, 'train_id': booking.train_id, 'seats_booked': booking.seats_booked}), 200
    return jsonify({'msg': 'Booking not found'}), 404

# Run server
if __name__ == '__main__':
    app.run(debug=True)
