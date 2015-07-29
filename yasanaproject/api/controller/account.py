

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as api_status
from account.core.serializers.user_serializer import UserSerializer
from account.core.forms.create_user_form import CreateUserForm


@api_view(['GET', 'POST'])
def api_get_users(request):

    if request.method == 'GET':
        try:
            page_num = int(request.GET.get('pg_no', 0))
        except ValueError:
            return Response(status=api_status.HTTP_400_BAD_REQUEST)
        else:
            if page_num < 0:
                page_num = 0
            non_admin_users = get_user_model().objects.filter(is_admin=False)
            return Response(UserSerializer(non_admin_users.order_by('-created_date')[page_num:page_num+10], many=True)
                            .data, status=api_status.HTTP_200_OK)
    else:
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_admin = False
            user.save()
            return Response({'save_status': True}, status=api_status.HTTP_200_OK)
        return Response({'save_status': form.errors}, status=api_status.HTTP_200_OK)


@api_view(['GET'])
def get_users_total_count(request):

    num_of_users = get_user_model().objects.filter(is_admin=False).count()

    return Response({'num_of_users': num_of_users}, status=api_status.HTTP_200_OK)
