

from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as api_status
from ..core.serializers.user_serializer import UserSerializer


def manage_users(request):
    return render(request, 'account/user-management.html')


def manage_users_partial(request):
    return render(request, 'account/partials/user-management.html')


@api_view(['GET'])
def api_get_users(request):
    print('In get users')
    return Response(UserSerializer(get_user_model().objects.all(), many=True).data, status=api_status.HTTP_200_OK)
