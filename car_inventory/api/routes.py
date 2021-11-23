from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import db, User, Car, car_schema, cars_schema


api = Blueprint('api',__name__, url_prefix ='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some':'value'}


# create car route
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    description = request.json['description']
    user_token = current_user_token.token

    car = Car(make, model, year, description, user_token)
    db.session.add(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}),401

@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id) #Get the drone instance

    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.description = request.json['description']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)    