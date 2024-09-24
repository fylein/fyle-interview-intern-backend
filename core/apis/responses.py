from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data=None, status_code=200, message=None):
        response_data = {'data': data}
        if message:
            response_data['message'] = message
        return make_response(jsonify(response_data), status_code)