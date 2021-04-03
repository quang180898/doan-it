from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.postgres.library.author.models import Author
from core.postgres.library.category.models import Category
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
                                           verbose_name=_('Publishing_company'))
    location = models.CharField(max_length=255, db_column='location', null=True, blank=True)
    description = models.CharField(max_length=1000, db_column='description', null=True, blank=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'book'
        verbose_name_plural = _('Book')
