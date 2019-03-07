from rest_framework.exceptions import APIException

class ValidityError(APIException):
    status_code = 200
    default_detail = ''
    default_code = ''