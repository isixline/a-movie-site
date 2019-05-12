from flask import jsonify
from . import bp


def bad_request(message='bad request'):
    return jsonify({'message': message}), 400


def forbidden(message='forbidden'):
    return jsonify({'message': message}), 403


@api.errorhandler(404)
def page_not_found(message="Not Found"):
    return jsonify({'message' : message}), 404

@api.errorhandler(500)
def page_not_found(message="Inter Server Error"):
    return jsonify({'message' : message}), 500

@api.errorhandler(401)
def unauthorized(message='unauthorized'):
    return jsonify({'message': message}), 401

