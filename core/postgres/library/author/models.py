from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.postgres.models import BaseModel


class Author(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True)
    mail = models.CharField(max_length=100, db_column='mail', null=True, blank=True)
    mobile = models.CharField(max_length=10, db_column='mobile', blank=True, null=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'author'
        verbose_name_plural = _('Author')
