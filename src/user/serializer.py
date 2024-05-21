from rest_framework import serializers
from user.models import forgotpassword, Profile


class forgotpasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = forgotpassword
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
