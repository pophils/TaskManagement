

from django.conf.urls import patterns, url
from .controller.user_management import user_collection_partial, add_user_partial

urlpatterns = patterns('',
                       url(r'^user-collection/', user_collection_partial, name='user_collection_partial'),
                       url(r'^add-user/', add_user_partial, name='add_user_partial'),
                       )
