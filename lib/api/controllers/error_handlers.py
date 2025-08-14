from flask import jsonify

def handle_exceptions(e):
    return jsonify({"message": "Bad Request"}), 400

def handle_validation_error(e):
    return jsonify({"message": "Bad Request: Invalid Input"}), 400

def handle_server_errors(e):
    return jsonify({"message": "Something went wrong"}), 500

def handle_custom_exceptions(e):
    response = {"message": e.message}
    if hasattr(e, "error_code"):
        response["error"] = e.error_code

    if hasattr(e, "duplicates") and e.duplicates:
        response["duplicates"] = e.duplicates

    return jsonify(response), e.status_code

def handle_not_found(e):
    return jsonify({"message": "Requested URL does not exist"}), 404