from rest_framework import  status
from api.models.models import Devices, Scores
from api.serializers.serializers import DeviceSerializer, UserSerializer, User
from rest_framework.response import Response
from api.logs import GenerateLogs
from django.db import transaction



LOGGER = GenerateLogs

def create_device(data):
    device_serializer = DeviceSerializer(data=data)
    ja3 = data.get('ja3')
    ja4 = data.get('ja4')
    ja4h = data.get('ja4h')
    source_ipv4 = data.get('source_ipv4')
    main = True
    if not device_serializer.is_valid():
        raise ValueError("Device serializer is not valid: {}".format(device_serializer.errors))
    device_serializer.save()
    device = Devices.objects.get(id= device_serializer.data.get("id"))
    score_data = {}
    score_data["is_safe"] = main
    score_data["score"] = 0
    score_data["current_score_enhanced"] = 0
    score_data["ja4"] = ja4
    score_data["ja4h"] = ja4h
    score_data["ja4l"] = None
    score_data["ja3"] = ja3
    score_data["get_header_signature"] = None
    score_data["post_header_signature"] = data.get("post_header_signature")
    score_data["content_length"] = data.get("content_length")
    score_data["source_ipv4"] = source_ipv4
    score_data["user_agent"] = data.get("user_agent")
    Scores.objects.create(device=device, **score_data)
    return device_serializer


def new_user(request, data, action):
        serializer = UserSerializer(data=data)
        if not data.get("pre-auth", False) and serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    LOGGER(request, "INFO", action).write_log('New user created')
                    response = Response(serializer.data, status=status.HTTP_201_CREATED)
                    user = User.objects.prefetch_related('devices').get(email=data.get('email'))
                    data['User'] = user.id
                    check = create_device(data)
                    if check == 'error':
                        raise Exception('Client did not send a successful request')
                    LOGGER(request, "INFO", action).write_log('New Device created')
                    user.active = True
                    user.save()
                    device = user.devices.latest('created_at')
                    device.verified = True
                    device.save()
                    return response
            except Exception as e:
                LOGGER(request, "ERROR", action).write_log(f'Atomic transaction failed: {str(e)}')
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif data.get("pre-auth", False):
            LOGGER(request, "INFO", action).write_log('unkown user in pre-auth')
            return Response({"message": "unkown user in pre-auth"}, status=status.HTTP_200_OK)
            
        LOGGER(request, "ERROR", action).write_log(
            'New user not created, error: {}'.format(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_417_EXPECTATION_FAILED)