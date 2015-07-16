
from django.db import models
from .abstract_base_entity import AbstractBaseEntity


class Organisation(AbstractBaseEntity, models.Model):
    org_id = models.AutoField(primary_key=True, db_index=True, auto_created=True)
    name = models.CharField(max_length=200, db_index=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)

    def __str__(self):
        return '{} located at {}'.format(self.name.capitalize(), self.address)

    class Meta:
        db_table = 'organisation'
