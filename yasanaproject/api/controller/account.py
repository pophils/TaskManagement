

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as api_status
from account.core.serializers.user_serializer import UserSerializer
from account.core.forms.create_user_form import CreateUserForm


@api_view(['GET', 'POST'])
def api_get_users(request):

    if request.method == 'GET':
        page_num = request.GET.get('pg_no', 0)
        return Response(UserSerializer(get_user_model().objects.all()[page_num:], many=True).data,
                        status=api_status.HTTP_200_OK)
    else:
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return Response({'save_status': True}, status=api_status.HTTP_200_OK)
        return Response({'save_status': form.errors}, status=api_status.HTTP_200_OK)
