from rest_framework import status
from api.models.models import Devices, User
from api.serializers.serializers import UserSerializer
from rest_framework.response import Response
from api.use_cases.score import calculate_permission
from api.utils import fail_occurred
from api.logs import GenerateLogs

LOGGER = GenerateLogs


def score_retriever(request, data, action: str, user:User):
    """ This function retrieves the minimum score from the user and the offensors that the user has """
    err = None
    # parte em que eu recebo o server side e adiciono um objeto no banco
    hash_checker, offensors, lower_score, lower_device = calculate_permission(request, data, user, action)
    if not hash_checker:
        LOGGER(request, "ERROR", action).suspicious_user_error(offensors)
        try:
            fail_occurred(data)
        except Exception as e:
            print(e)
        print("offensors", offensors, "lower_score", lower_score, "lower_device", lower_device, "error aqui 1", )
        err = Response({'score':lower_score, "offensors": str(offensors), 'imunex-user':user.email}, status=status.HTTP_400_BAD_REQUEST)
    return hash_checker, offensors, lower_score, lower_device, err


def validate_user(request, data, user:User, action):
    user = user
    # parte em que eu verifico se o server side já fez a request pra gente
    _, _, lower_score, _, err = score_retriever(request, data, action, user)
    if err:
        return err

    serializer = UserSerializer(user, data=data)
    if not serializer.is_valid():
        LOGGER(request, "ERROR", action).write_log('User not updated, error: {}'.format(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_417_EXPECTATION_FAILED)
    
    serializer.save()
    LOGGER(request, "INFO", action).write_log('User updated')
    return Response({"score": lower_score}, status=status.HTTP_200_OK)
        