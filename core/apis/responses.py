from flask import Response, jsonify, make_response

class APIResponse(Response):
    @classmethod
    def respond(cls, data=None, status_code=200):
        response = jsonify(data=data)
        response.status_code = status_code
        return response
    
    @classmethod
    def respond_error(cls, message, status_code):
        response = jsonify({'error': message})
        response.status_code = status_code
        return response
