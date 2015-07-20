

from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY, authenticate
from django.contrib.sessions.models import SessionStore


def create_pre_authenticated_session(email, first_name, password):

    user = get_user_model().objects.create_user(email=email, first_name=first_name, password=password)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()

    return session.session_key
