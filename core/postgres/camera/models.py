from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.postgres.models import BaseModel
from library.constant.api import CAMERA_NOT_RECORD, CAMERA_RECORDING_CHOICE


class Camera(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    camera_vms = models.IntegerField(db_column='vms_camera_id', blank=True)
    name = models.CharField(max_length=150, db_column='name', blank=True)
    # camera_type = models.ForeignKey(CameraType, db_column='camera_type_id',
    #                                 blank=True, null=True,
    #                                 on_delete=models.PROTECT,
    #                                 verbose_name=_('Camera Type'))
    province_id = models.IntegerField(db_column='province_id', blank=True,
                                      null=True, verbose_name=_('Province'))
    district_id = models.IntegerField(db_column='district_id', blank=True,
                                      null=True, verbose_name=_('District'))
    ward_id = models.IntegerField(db_column='ward_id', blank=True,
                                  null=True, verbose_name=_('Ward'))
    latitude = models.FloatField(db_column='latitude', default=0,
                                 blank=True, null=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(db_column='longitude', default=0,
                                  blank=True, null=True, verbose_name=_('Longitude'))
    recording = models.IntegerField(db_column='recording', default=CAMERA_NOT_RECORD,
                                    blank=True, null=True,
                                    choices=CAMERA_RECORDING_CHOICE)
    firmware = models.CharField(max_length=255, db_column='firmware', null=True, blank=True, verbose_name=_('Firmware'))
    manufacturer = models.CharField(max_length=255, db_column='manufacturer', null=True, blank=True,
                                    verbose_name=_('Manufacturer'))
    mac = models.CharField(max_length=255, db_column='mac', null=True, blank=True, verbose_name=_('Mac'))
    model = models.CharField(max_length=255, db_column='model', null=True, blank=True, verbose_name=_('Model'))

    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    active_flag = models.BooleanField(db_column='active_flag', default=True)
    url_stream = models.CharField(max_length=255, db_column='url_stream', null=True, blank=True)
    coordinates = models.JSONField(db_column='coordinates', blank=True, null=True)
    slug = models.UUIDField(db_column='slug', null=True, blank=True, editable=False)

    class Meta(BaseModel.Meta):
        db_table = 'cctv_camera'
        verbose_name_plural = _('Camera')
