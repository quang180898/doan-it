from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.postgres.models import BaseModel
from library.constant.api import CAMERA_NOT_RECORD, CAMERA_RECORDING_CHOICE


class Book(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True)
    # camera_type = models.ForeignKey(CameraType, db_column='camera_type_id',
    #                                 blank=True, null=True,
    #                                 on_delete=models.PROTECT,
    #                                 verbose_name=_('Camera Type'))
    quantity = models.IntegerField(db_column='quantity', null=True, blank=True)
    price = models.FloatField(db_column='price', null=True, blank=True)


    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    active_flag = models.BooleanField(db_column='active_flag', default=True)
    url_stream = models.CharField(max_length=255, db_column='url_stream', null=True, blank=True)
    coordinates = models.JSONField(db_column='coordinates', blank=True, null=True)
    slug = models.UUIDField(db_column='slug', null=True, blank=True, editable=False)

    class Meta(BaseModel.Meta):
        db_table = 'cctv_camera'
        verbose_name_plural = _('Camera')
