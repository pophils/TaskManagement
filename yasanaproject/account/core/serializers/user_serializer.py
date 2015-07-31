

from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('get_full_name', read_only=True)

    @staticmethod
    def get_full_name(obj):
        return obj.get_full_name()

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'department', 'phone', 'image_src', 'first_name', 'other_name', 'last_name',
                  'gender', 'website')
