

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as api_status
from account.core.serializers.user_serializer import UserSerializer


@api_view(['GET'])
def api_get_users(request):
    page_num = request.GET.get('pg_no', 0)

    return Response(UserSerializer(get_user_model().objects.all()[page_num:], many=True).data,
                    status=api_status.HTTP_200_OK)
