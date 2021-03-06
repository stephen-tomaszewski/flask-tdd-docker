from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from project import db
from project.api.models import User

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

# wrapper around SQLAlchemy model to enable payload validation
user = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):

    # validate param allows validation and throws error otherwise
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = User.query.filter_by(email=email).first()
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400
        db.session.add(User(username=username, email=email))
        db.session.commit()
        response_object["message"] = f"{email} was added!"
        return response_object, 201

    @api.marshal_with(user, as_list=True)
    def get(self):
        return User.query.all(), 200


class Users(Resource):
    # https://flask-restx.readthedocs.io/en/stable/marshalling.html
    # TODO when does marshal convert dict to bytes?
    @api.marshal_with(user)
    def get(self, user_id):
        return User.query.filter_by(id=user_id).first(), 200


api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<int:user_id>")
