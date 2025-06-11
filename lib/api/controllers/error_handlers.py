from flask import jsonify

def handle_exceptions(e):
    return jsonify({"message": "Bad request"}), 400

def handle_validation_error(e):
    return jsonify({"message": "Bad Request: Invalid Input"}), 400

def handle_server_errors(e):
    return jsonify({"message": "Something went wrong"}), 500

def handle_custom_exceptions(e):
    return jsonify({"message": e.message}), e.status_code