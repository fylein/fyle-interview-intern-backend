class FyleError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}

    def __str__(self):
        return f"FyleError(status_code={self.status_code}, message='{self.message}')"
