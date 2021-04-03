from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.postgres.models import BaseModel


class PublishingCompany(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True, null=True)
    email = models.CharField(max_length=150, db_column='email', blank=True, null=True)
    mobile = models.IntegerField(db_column='mobile', blank=True, null=True)
    address = models.CharField(max_length=150, db_column='address', blank=True, null=True)
    description = models.CharField(max_length=1000, db_column='description', null=True, blank=True)

    class Meta(BaseModel.Meta):
        db_table = 'publishing_company'
        verbose_name_plural = _('Publishing Company')
