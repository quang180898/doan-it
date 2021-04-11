from django.db.models import F

from api.base.apiViews import APIView
from config.settings import DATA_UPLOAD_MAX_MEMORY_SIZE
from core.postgres.library.book.models import Book
from core.postgres.library.permission.models import Permission
from library.constant.api import (
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_USER_NAME_DUPLICATE, SERVICE_CODE_NOT_FOUND, SERVICE_CODE_CUSTOMER_NOT_EXIST,
    SERVICE_CODE_NOT_EXISTS_USER, ADMIN, SERVICE_CODE_FILE_SIZE, SERVICE_CODE_FORMAT_NOT_SUPPORTED,
)
from library.functions import convert_to_int
from library.service.upload_file import get_constant_file_type_from_extension


class LibraryBook(APIView):
    def list_book(self, request):
        book = Book.objects.filter(
            deleted_flag=False
        ).annotate(
            category_id=F('bookcategory__category_id'),
            category_name=F('bookcategory__category_id__name'),
            author_id=F('bookauthor__author_id'),
            author_name=F('bookauthor__author_id__name')
        ).values(
            'id',
            'name',
            'image_bytes',
            'deleted_flag',
            'category_id',
            'category_name',
            'author_id',
            'author_name',
            'quantity',
            'price'
        )
        return self.response(self.response_success(list(book)))
