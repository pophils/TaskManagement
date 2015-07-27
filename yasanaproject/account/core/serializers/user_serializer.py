

from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('get_full_name', read_only=True)

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = UserProfile
        fields = ('email', 'name', 'department', 'phone', 'image_src')
