from flask import jsonify


class APIResponse:
    @staticmethod
    def respond(data=None):
        return jsonify({'data': data}), 200

    @staticmethod
    def respond_error(message, status_code):
        return jsonify({'error': 'Error', 'message': message}), status_code
