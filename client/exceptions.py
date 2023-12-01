from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = 400

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)