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
    # category = models.ForeignKey(Category, db_column='category',
    #                              blank=True, null=True,
    #                              on_delete=models.PROTECT,
    #                              verbose_name=_('Category'))
    # author = models.ForeignKey(Author, db_column='author',
    #                            blank=True, null=True,
    #                            on_delete=models.PROTECT,
    #                            verbose_name=_('Author'))
    # publishing_company = models.ForeignKey(PublishingCompany,
    #                                        db_column='publishing_company',
    #                                        blank=True, null=True,
    #                                        on_delete=models.PROTECT,
    #                                        verbose_name=_('Publishing_company'))
    location = models.CharField(max_length=255, db_column='location', null=True, blank=True)
    description = models.CharField(max_length=1000, db_column='description', null=True, blank=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'book'
        verbose_name_plural = _('Book')


class BookUser(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    book_id = models.ForeignKey(Book, db_column='book_id',
                                blank=True, null=True,
                                on_delete=models.PROTECT,
                                verbose_name=_('BookID'))
    user_id = models.ForeignKey(Customer, db_column='user_id',
                                blank=True, null=True,
                                on_delete=models.PROTECT,
                                verbose_name=_('UserID'))
    date_borrow = models.DateTimeField(db_column='date_borrow', blank=True, null=True)
    date_return = models.DateTimeField(db_column='date_return', blank=True, null=True)
    finished_flag = models.BooleanField(db_column='finished_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'customer_book'
        verbose_name_plural = _('Customer Book')


class BookAuthor(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    book_id = models.ForeignKey(Book, db_column='book_id',
                                blank=True, null=True,
                                on_delete=models.PROTECT,
                                verbose_name=_('BookID'))
    author_id = models.ForeignKey(Author, db_column='author_id',
                                  blank=True, null=True,
                                  on_delete=models.PROTECT,
                                  verbose_name=_('AuthorID'))

    class Meta(BaseModel.Meta):
        db_table = 'author_book'
        verbose_name_plural = _('Author Book')


class BookCategory(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    book_id = models.ForeignKey(Book, db_column='book_id',
                                blank=True, null=True,
                                on_delete=models.PROTECT,
                                verbose_name=_('BookID'))
    category_id = models.ForeignKey(Category, db_column='category_id',
                                    blank=True, null=True,
                                    on_delete=models.PROTECT,
                                    verbose_name=_('CategoryID'))

    class Meta(BaseModel.Meta):
        db_table = 'category_book'
        verbose_name_plural = _('Category Book')


class BookPublishing(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    book_id = models.ForeignKey(Book, db_column='book_id',
                                blank=True, null=True,
                                on_delete=models.PROTECT,
                                verbose_name=_('BookID'))
    publishing_company_id = models.ForeignKey(PublishingCompany, db_column='publishing_company_id',
                                              blank=True, null=True,
                                              on_delete=models.PROTECT,
                                              verbose_name=_('PublishingCompanyID'))

    class Meta(BaseModel.Meta):
        db_table = 'publishing_book'
        verbose_name_plural = _('Publishing Book')
