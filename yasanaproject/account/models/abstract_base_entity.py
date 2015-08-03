
from django.db import models


class AbstractBaseEntity(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
