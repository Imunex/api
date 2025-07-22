from api.serializers.serializers import UserSerializer
from drf_yasg import openapi


### UserViewSet create
new_user = openapi.Response("New User Created", UserSerializer)
success = openapi.Response("Account Verified and Safe", UserSerializer)
error = openapi.Response("Account Verified but not Safe")
sentt = openapi.Response("Activation Code Aready sent but Account not verified yet")
unauth = openapi.Response("Missing/Invalid Api Key ")
prerec = openapi.Response("Missing/Invalid data to create/update imunex user")
create_user_responses=openapi.Responses({200:success, 201:new_user, 400:error, 406:sentt, 401:unauth, 417:prerec })


### DeviceViewSet create
success = openapi.Response("Standard Request Success", UserSerializer)
unauth = openapi.Response("Missing/Invalid Api Key ")
prerec = openapi.Response("Email missing in the query params")
error = openapi.Response("Suspicious request from source")
create_device_responses=openapi.Responses({200:success, 400:error, 401:unauth, 417:prerec })


### DeviceViewSet delete
success_delete = openapi.Response(description="Standard Request Success")
not_f=openapi.Response("Device not found")
delete_devices_response=openapi.Responses({204:success_delete, 400:error, 401:unauth, 404:not_f })

## Device Activation
inv_code = openapi.Response("Invalid Code")
success = openapi.Response("Account activated successfully")
expired = openapi.Response("Activation Code Expired")
activate_account_responses=openapi.Responses({200:success, 406:inv_code, 400:expired})