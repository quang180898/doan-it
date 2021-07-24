from django.db.models import F, Q

from api.base.apiViews import APIView
from config.settings import DATA_UPLOAD_MAX_MEMORY_SIZE
from core.postgres.library.book.models import Book, BookUser
from core.postgres.library.permission.models import Permission
from library.constant.api import (
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_USER_NAME_DUPLICATE, SERVICE_CODE_NOT_FOUND, SERVICE_CODE_CUSTOMER_NOT_EXIST,
    SERVICE_CODE_NOT_EXISTS_USER, ADMIN, SERVICE_CODE_FILE_SIZE, SERVICE_CODE_FORMAT_NOT_SUPPORTED,
    SERVICE_CODE_BOOK_NOT_EXIST,
)
from library.functions import convert_to_int, convert_string_to_list, convert_to_float, get_thumbnail, \
    convert_byte_to_base64
from library.service.upload_file import get_constant_file_type_from_extension


class LibraryBook(APIView):
    def list_book(self, request):
        book_name = self.request.query_params.get('book_name')
        category_id = self.request.query_params.get('category_id')
        author_id = self.request.query_params.get('author_id')
        book = Book.objects.filter(deleted_flag=False)
        if book_name:
            book = book.filter(name__icontains=book_name)
        if category_id:
            book = book.filter(category_id=category_id)
        if author_id:
            book = book.filter(author_id=author_id)

        book = book.annotate(
            category_name=F('category__name'),
            author_name=F('author__name'),
            publishing_company_name=F('publishing_company__name'),
        ).values(
            'id',
            'name',
            'location',
            'category_id',
            'category_name',
            'author_id',
            'author_name',
            'publishing_company_id',
            'publishing_company_name',
            'quantity',
            'price',
            'image_bytes'
        ).order_by('id')
        for img in book:
            base64 = convert_byte_to_base64(img['image_bytes'])
            img['image_bytes'] = base64
        self.pagination(book)
        return self.response(self.response_paging(self.paging_list))

    def detail_book(self, request):
        book_id = convert_to_int(self.request.query_params.get('book_id'))
        book = Book.objects.filter(id=book_id, deleted_flag=False)
        if book:
            book = book.annotate(
                category_name=F('category__name'),
                author_name=F('author__name'),
                publishing_company_name=F('publishing_company__name'),
            ).values(
                'id',
                'name',
                'location',
                'description',
                'price',
                'quantity',
                'category_id',
                'category_name',
                'author_id',
                'author_name',
                'publishing_company_id',
                'publishing_company_name',
                'image_bytes'
            ).order_by('id').first()
            book['image_bytes'] = convert_byte_to_base64(book['image_bytes'])
            return self.response(self.response_success(book))
        else:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND)

    def book_same_category(self, request):
        book_id = convert_to_int(self.request.query_params.get('book_id'))
        try:
            book_category = Book.objects.get(id=book_id, deleted_flag=False)
        except Book.DoesNotExist:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND)
        book_same_category = Book.objects.filter(
            ~Q(id=book_id),
            Q(category_id=book_category.category_id),
            Q(deleted_flag=False)
        ).values(
            'id',
            'name',
            'price',
            'category_id',
            'category__name',
            'quantity',
            'image_bytes'
        ).order_by('id')
        for item in book_same_category:
            base64 = convert_byte_to_base64(item['image_bytes'])
            item['image_bytes'] = base64
        return self.response(self.response_success(list(book_same_category)))

    def create_or_update(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.data
        except:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR)

        key_content_list = list(content.keys())
        check_keys_list = ['name', 'price', 'category_id', 'author_id', 'publishing_company_id', 'quantity', 'location']
        book_id = content.get('book_id')
        name = content.get('name')
        description = content.get('description')
        price = convert_to_float(content.get('price'))
        category_id = convert_to_int(content.get('category_id'))
        author_id = convert_to_int(content.get('author_id'))
        publishing_company_id = convert_to_int(content.get('publishing_company_id'))
        location = content.get('location')
        quantity = convert_to_int(content.get('quantity'))
        image = request.FILES['image'] if request.FILES.get('image') else None
        image_name = content.get('image_name')

        if image:
            if image_name is None:
                return self.validate_exception("missing image_name!")

            img = image_name.split('.')[-1]
            image_name = get_constant_file_type_from_extension(img)
            if image_name is None:
                return self.response_exception(code=SERVICE_CODE_FORMAT_NOT_SUPPORTED)
            size = request.headers['content-length']
            if int(size) > DATA_UPLOAD_MAX_MEMORY_SIZE:
                return self.response_exception(code=SERVICE_CODE_FILE_SIZE)
        if book_id:
            try:
                book = Book.objects.get(id=book_id, deleted_flag=False)
            except Book.DoesNotExist:
                return self.response_exception(code=SERVICE_CODE_NOT_FOUND)
            book.name = name if name is not None else book.name
            book.description = description if description is not None else book.description
            book.location = location if location is not None else book.location
            book.price = price if price > 0.0 else book.price
            book.category_id = category_id if category_id != 0 else book.category_id
            book.author_id = author_id if author_id != 0 else book.author_id
            book.publishing_company_id = publishing_company_id if publishing_company_id != 0 else book.publishing_company_id
            book.quantity = quantity if quantity != 0 else book.quantity
            if image:
                book.image_bytes = image.read()
            book.save()
            return self.response(self.response_success({
                "book_id": book.id,
                "book_name": book.name,
                "book_location": book.location,
                "book_description": book.description,
                "book_category_id": book.category_id,
                "book_author_id": book.author_id,
                "book_publishing_company_id": book.publishing_company_id,
                'image_bytes': book.get_image
            }))
        else:
            if not all(key in key_content_list for key in check_keys_list):
                return self.validate_exception(
                    'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))
            book_new = Book.objects.create(
                name=name,
                description=description,
                price=price,
                location=location,
                category_id=category_id,
                author_id=author_id,
                publishing_company_id=publishing_company_id,
                quantity=quantity,
                image_bytes=image.read()
            )
            return self.response(self.response_success({
                "book_id": book_new.id,
                "book_name": book_new.name,
                "book_location": book_new.location,
                "book_description": book_new.description,
                "book_category_id": book_new.category_id,
                "book_author_id": book_new.author_id,
                "book_publishing_company_id": book_new.publishing_company_id,
                "book_price": book_new.price,
                "book_quantity": book_new.quantity,
                'image_bytes': book_new.get_image
            }))

    def delete_book(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        book_id = content.get('book_id')
        delete = Book.objects.filter(id=book_id, deleted_flag=False).first()
        if delete:
            book_user = BookUser.objects.filter(book_id=book_id, deleted_flag=False)
            if book_user:
                book_user.update(deleted_flag=True)
            delete.deleted_flag = True
            delete.save()
            return self.response(self.response_success("Success!"))
        else:
            return self.response_exception(code=SERVICE_CODE_BOOK_NOT_EXIST)
