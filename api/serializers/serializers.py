from rest_framework import serializers
from api.models.models import Devices, Scores, TimeStamp, User

class TimeStampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStamp
        fields = ('created_at' , 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        first_email = data['email'].split('@')[0]
        data['friendly_name'] = first_email
        return data
    
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = "__all__"

class ScoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Scores
        fields = "__all__"
