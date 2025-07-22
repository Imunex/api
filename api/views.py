
from django.utils.decorators import method_decorator
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework_api_key.permissions import HasAPIKey
from drf_yasg.utils import swagger_auto_schema

from api.authentication import verify_authorization, verify_dec
from api.logs import GenerateLogs
from api.models.models import User
from api.serializers.serializers import UserSerializer
from api.use_cases.new_user import new_user
from api.use_cases.current_user import validate_user
from api.utils import is_account_new, set_data
from rest_framework.permissions import AllowAny


LOGGER = GenerateLogs      

@method_decorator([verify_dec], name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = [AllowAny]
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        """
            This endpoint is responsible for all major uses of the Imunex API. 
            To use this endpoint correctly you have to send the same request that was sent to the backend that you want to analyse. 
            The difference is that you can ommit the user's password.
            All HTTP Headers must be included in the same order that they were sent.
            Initially it will analyse if its a new user or a current user. If it is a new user
            the system will send an e-mail for the user to verificate that he is coming from a safe device.
            If it is a current user the system will check if the user is in the safe device or from a not trusted source.
            Then the system will return the score for this attempt.
        """
        action = "Creating/Login Account"
        data = request.data.copy()
        data['email'] = data.get('email')
        data = set_data(data, request)
        new_checker, imunex_user = is_account_new(data)
        if new_checker:
            return new_user(request, data, action)
        else:
            return validate_user(request, data, imunex_user, action)
        
    @swagger_auto_schema(auto_schema=None)
    def list(self, request):
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk=None):
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    def options(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
