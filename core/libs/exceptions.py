# class FyleError(Exception):
#     status_code = 400

#     def __init__(self, status_code, message):
#         Exception.__init__(self)
#         self.message = message
#         self.status_code = status_code

#     def to_dict(self):
#         res = dict()
#         res['message'] = self.message
#         return res


class FyleError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)  # Call the base class constructor
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}
