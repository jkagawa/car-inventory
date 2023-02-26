from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, car_multi_schema, user_schema

api = Blueprint('ap', __name__, url_prefix='/api')

# Add new car endpoint
@api.route('/car', methods = ['POST'])
@token_required
def add_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    user_token = current_user_token.token

    print(f'User\'s token: {current_user_token.token}')

    try:
        car = Car(make, model, year, user_token)
        db.session.add(car)
        db.session.commit()

        response = car_schema.dump(car)
        return jsonify(response)
    except:
        return jsonify({'message' : 'Failed to add item'}), 500

# Get all cars added by user
@api.route('/car', methods = ['GET'])
@token_required
def get_car(current_user_token):
    user_token = current_user_token.token
    car = Car.query.filter_by(user_token=user_token).all()
    if car:
        response = car_multi_schema.dump(car)
        return jsonify(response)
    return jsonify({'message' : 'Item not found'}), 404

# Get single car added by user
@api.route('/car/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    user_token = current_user_token.token
    car = Car.query.filter_by(user_token=user_token, id=id).all()
    if car:
        response = car_schema.dump(car)
        return jsonify(response)
    return jsonify({'message' : 'Item not found'}), 404
    
# Update car endpoint
@api.route('/car/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token, id):
    user_token = current_user_token.token
    car = Car.query.filter_by(user_token=user_token, id=id).all()
    if car:
        car.make = request.json['make']
        car.model = request.json['model']
        car.year = request.json['year']
        car.user_token = current_user_token.token

        db.session.commit()
        response = car_schema.dump(car)
        return jsonify(response)
    return jsonify({'message' : 'Item not found'}), 404

# Delete car endpoint
@api.route('/car/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    user_token = current_user_token.token
    car = Car.query.get(id)
    if car and car.user_token == user_token:
        db.session.delete(car)
        db.session.commit()
        response = car_schema.dump(car)
        return jsonify(response)
    return jsonify({'message' : 'Item not found'}), 404

# Delete user endpoint
@api.route('/user/<id>', methods = ['DELETE'])
@token_required
def delete_user(current_user_token, id):
    user_token = current_user_token.token
    user = User.query.get(id)
    if user and user.token == user_token:
        db.session.delete(user)
        db.session.commit()
        response = user_schema.dump(user)
        return jsonify(response)
    return jsonify({'message' : 'User not found'}), 404