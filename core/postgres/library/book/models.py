import base64
import datetime
import io

from PIL import Image
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.postgres.library.author.models import Author
from core.postgres.library.category.models import Category
from core.postgres.library.customer.models import Customer
from core.postgres.library.publishing_company.models import PublishingCompany
from core.postgres.models import BaseModel


class Book(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True)
    quantity = models.IntegerField(db_column='quantity', null=True, blank=True)
    price = models.FloatField(db_column='price', null=True, blank=True)
    category = models.ForeignKey(Category, db_column='category',
                                 blank=True, null=True,
                                 on_delete=models.PROTECT,
                                 verbose_name=_('Category'))
    author = models.ForeignKey(Author, db_column='author',
                               blank=True, null=True,
                               on_delete=models.PROTECT,
                               verbose_name=_('Author'))
    publishing_company = models.ForeignKey(PublishingCompany,
                                           db_column='publishing_company',
                                           blank=True, null=True,
                                           on_delete=models.PROTECT,
                                           verbose_name=_('Publishing Company'))
    location = models.CharField(max_length=255, db_column='location', null=True, blank=True)
    description = models.CharField(max_length=1000, db_column='description', null=True, blank=True)
    image_bytes = models.BinaryField(db_column='image_bytes')
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'book'
        verbose_name_plural = _('Book')

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


class BookUser(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    book = models.ForeignKey(Book, db_column='book_id',
                             blank=True, null=True,
                             on_delete=models.PROTECT,
                             verbose_name=_('BookID'))
    user = models.ForeignKey(Customer, db_column='user_id',
                             blank=True, null=True,
                             on_delete=models.PROTECT,
                             verbose_name=_('UserID'))
    date_borrow = models.DateTimeField(db_column='date_borrow', blank=True, null=True)
    date_return = models.DateTimeField(db_column='date_return', blank=True, null=True)
    finished_flag = models.BooleanField(db_column='finished_flag', default=False)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    status = models.CharField(max_length=20, db_column='status', default='Chưa tới hạn')

    class Meta(BaseModel.Meta):
        db_table = 'customer_book'
        verbose_name_plural = _('Customer Book')

    def set_status(self):
        now = datetime.datetime.now()
        if self.finished_flag is True:
            return self.status == 'Đã Trả'
        else:
            if self.date_return <= now:
                return self.status == 'Trễ Hạn'
