#!/usr/bin/env python3

from flask import request, session, make_response, jsonify
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username'],
            _password_hash=json['password']
        )
        db.session.add(user)
        db.session.commit()
        user_dict = User.query.filter(User.username == user.username).first().to_dict()
        session['user_id'] = user_dict['id']
        return make_response(user_dict, 201)

class CheckSession(Resource):
    def get(self):
        user_id = session['user_id']
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return make_response(user.to_dict(), 200)
        return {}, 204
    
class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        user = User.query.filter(User.username == username).first()

        if user:
            session['user_id'] = user.id
            return make_response(jsonify(user.to_dict()), 200)

        return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Login, '/login', endpoint='login')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
