from api.logs import GenerateLogs
from typing import Union
from rest_framework import  status
from rest_framework.response import Response
from django.http import HttpResponse


LOGGER = GenerateLogs      

#this has no security, it just check if the authorization header is present and has a space
def verify_authorization(request) -> Union[dict[str, bool], None]:
    """
    This function verifies the authorization
    """
    api_key = request.headers.get('Authorization')
    if  type(api_key) != str or " " not in api_key:
        return {"failed":True}
    first_part = api_key.split(' ')[0]
    if not first_part:
        return {"failed":True,}
    return {"failed":False}


def verify_dec(func):
    def wrapper(request, *args, **kwargs):
        verify = verify_authorization(request)
        if verify["failed"]:
            return HttpResponse('"Authorization or Authentication failed"', content_type="application/json", status=401)
        return func(request, *args, **kwargs)
    return wrapper

