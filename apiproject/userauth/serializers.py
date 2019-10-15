from rest_framework import serializers
from .models import CustomUser,UserOtp

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =('email', 'username',)

class OtpSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserOtp
		fields = ('email',)


class OtpValidateSerializer(serializers.Serializer):
	email =serializers.EmailField(max_length=20)
	otp = serializers.CharField(max_length=6)