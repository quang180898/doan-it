from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.postgres.models import BaseModel
from library.constant.api import GENDER_TYPE_MALE, GENDER_TYPE_CHOICE


class Customer(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True)
    username = models.CharField(max_length=50, db_column='username', null=True, blank=True)
    password = models.CharField(max_length=255, db_column='password', null=True, blank=True)
    mail = models.CharField(max_length=255, db_column='mail', null=True, blank=True)
    mobile = models.CharField(max_length=255, db_column='mobile', null=True, blank=True)
    address = models.CharField(max_length=255, db_column='address', null=True, blank=True)
    permission = models.ForeignKey(Permission, db_column='permission_id',
                                   blank=True, null=True,
                                   on_delete=models.PROTECT,
                                   verbose_name=_('Permission'))
    gender = models.IntegerField(db_column='gender',
                                 default=GENDER_TYPE_MALE,
                                 blank=True, null=True,
                                 choices=GENDER_TYPE_CHOICE)
    birthdate = models.DateTimeField(db_column='birthdate', null=True, blank=True)
    description = models.CharField(max_length=1000, db_column='description', null=True, blank=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    active_flag = models.BooleanField(db_column='active_flag', default=True)

    class Meta(BaseModel.Meta):
        db_table = 'customer'
        verbose_name_plural = _('Customer')
