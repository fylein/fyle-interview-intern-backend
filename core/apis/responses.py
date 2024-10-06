from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data, status=200):
        if status == 400 or status == 404:
            return make_response(data, status)
        return make_response(jsonify(data=data), status)
