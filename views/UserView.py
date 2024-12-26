from flask import request, Blueprint, jsonify
from models.UserModel import UserModel, UserSchema

user_blueprint = Blueprint("users", __name__, url_prefix="/users")
user_schema = UserSchema()


@user_blueprint.route('/', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        result = UserModel.query.all()
        return jsonify(user_schema.dump(result, many=True)), 200

    elif request.method == 'POST':
        data = request.json
        errors = user_schema.validate(data)
        if errors:
            return jsonify(Error="User name cannot be empty"), 400
        else:
            user = UserModel(data.get("user_id"), data.get("user_name"))
            if user.add():
                return jsonify(Message="User registered successfully"), 201
            else:
                return jsonify(Error="User with same id already exists"), 400


@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserModel.query.get(user_id)
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify(Message='No user with that ID'), 400


@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    if user:
        user.delete()
        return jsonify(Message="Success"), 204
    else:
        return jsonify(Error='No user with that ID'), 400
