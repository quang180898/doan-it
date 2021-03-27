from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.postgres.camera_detect_type.models import DetectType
from core.postgres.customer.models import Customer
from core.postgres.models import BaseModel
from core.postgres.vms.models import VMS, VmsGroup
from library.constant.api import CAMERA_NOT_RECORD, CAMERA_RECORDING_CHOICE


class CameraType(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True)

    class Meta(BaseModel.Meta):
        db_table = 'cctv_camera_type'
        verbose_name_plural = _('Camera Type')


class Camera(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    vms = models.ForeignKey(VMS, db_column='vms_id',
                            blank=True, null=True,
                            on_delete=models.PROTECT,
                            verbose_name=_('VMS'))
    camera_group = models.ForeignKey(VmsGroup, db_column='camera_group_id',
                                     blank=True, null=True,
                                     on_delete=models.PROTECT,
                                     verbose_name=_('Camera Group'))
    camera_vms = models.IntegerField(db_column='vms_camera_id', blank=True)
    name = models.CharField(max_length=150, db_column='name', blank=True)
    camera_type = models.ForeignKey(CameraType, db_column='camera_type_id',
                                    blank=True, null=True,
                                    on_delete=models.PROTECT,
                                    verbose_name=_('Camera Type'))
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


class CameraUser(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    camera = models.ForeignKey(Camera, db_column='camera_id',
                               blank=True, null=True,
                               on_delete=models.PROTECT,
                               verbose_name=_('Camera'),
                               related_name="camera_user")
    user = models.ForeignKey(Customer, db_column='user_id',
                             blank=True, null=True,
                             on_delete=models.PROTECT,
                             verbose_name=_('Customer'))
    view_flag = models.BooleanField(db_column='view_flag', default=True)
    edit_flag = models.BooleanField(db_column='edit_flag', default=False)
    active_flag = models.BooleanField(db_column='active_flag', default=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'cctv_camera_user'
        verbose_name_plural = _('Camera User')


class CameraDetect(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    camera = models.ForeignKey(Camera, db_column='camera_id',
                               blank=True, null=True,
                               on_delete=models.PROTECT,
                               verbose_name=_('Camera'))
    detect = models.ForeignKey(DetectType, db_column='detect_id',
                               blank=True, null=True,
                               on_delete=models.PROTECT,
                               verbose_name=_('Detect'))
    active_flag = models.BooleanField(db_column='active_flag', default=True)

    class Meta(BaseModel.Meta):
        db_table = 'cctv_camera_detect'
        verbose_name_plural = _('Camera Detect')


class CameraDrawArea(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    camera = models.ForeignKey(Camera, db_column='camera_id',
                               blank=True, null=True,
                               on_delete=models.PROTECT,
                               verbose_name=_('Camera'))
    name = models.CharField(max_length=255, db_column='name', null=True, blank=True)
    type_draw = models.IntegerField(db_column='type_draw', null=True, blank=True)
    coordinates = models.JSONField(db_column='coordinates', blank=True, null=True)
    camera_width = models.IntegerField(db_column='camera_width', blank=True, null=True)
    camera_height = models.IntegerField(db_column='camera_height', blank=True, null=True)

    class Meta(BaseModel.Meta):
        db_table = 'cctv_camera_draw_area'
        verbose_name_plural = _('Camera Draw Area')
