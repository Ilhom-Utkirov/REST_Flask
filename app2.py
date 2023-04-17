import os

from flask import Flask
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'  # cz we are working with security issues we use it
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)


api = Api(app)
jwt = JWT(app, authenticate, identity)

# [ {'name':"Rufus"},{'name':"Reks"} ]
puppies = []




class PuppyNames(Resource):
    # same arguments
    def get(self, name):
        for pup in puppies:
            if pup['name'] == name:
                return pup
        return {'name': None}, 404  # send http status 404

    def post(self, name):
        pup = {'name': name}
        puppies.append(pup)
        return pup

    def delete(self, name):
        for ind, pup in enumerate(puppies):
            if pup['name'] == name:
                deleted_pup = puppies.pop(ind)
                return {'note': 'delete success'}


class AllNames(Resource):
    #provide username, password and get authenticated
    @jwt_required()
    def get(self):
        return {'puppies': puppies}


# app.route = api.add_resource
api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames, '/puppies')

if __name__ == '__main':
    app.run(debug=True)
