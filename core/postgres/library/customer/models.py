import base64
import io
from PIL import Image
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.postgres.library.permission.models import Permission
from core.postgres.models import BaseModel
from library.constant.api import GENDER_TYPE_MALE, GENDER_TYPE_CHOICE


class Customer(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True)
    username = models.CharField(max_length=50, db_column='username', null=True, blank=True)
    password = models.CharField(max_length=255, db_column='password', null=True, blank=True)
    mail = models.CharField(max_length=255, db_column='mail', null=True, blank=True)
    mobile = models.CharField(max_length=10, db_column='mobile', blank=True, null=True)
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
    image_bytes = models.BinaryField(db_column='image_bytes')
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    active_flag = models.BooleanField(db_column='active_flag', default=True)

    class Meta(BaseModel.Meta):
        db_table = 'customer'
        verbose_name_plural = _('Customer')

    @property
    def get_image(self):
        try:
            return base64.b64encode(self.image_bytes).decode('utf-8')
        except:
            return None

    @property
    def get_thumbnail(self):
        try:
            image = Image.open(io.BytesIO(self.image_bytes))
            image.thumbnail((90, 90))
            data = io.BytesIO()
            image.save(data, format="PNG")
            return base64.b64encode(data.getvalue()).decode('utf-8')
        except:
            return None
