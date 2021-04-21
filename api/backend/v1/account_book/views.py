import datetime

from django.db.models import F
from django.utils import timezone

from api.base.apiViews import APIView
from core.postgres.library.book.models import Book, BookUser
from core.postgres.library.customer.models import Customer
from library.constant.api import SERVICE_CODE_NOT_EXISTS_BODY, SERVICE_CODE_BODY_PARSE_ERROR, \
    SERVICE_CODE_RECORD_NOT_VALIDATE, SERVICE_CODE_NOT_EXISTS_USER, SERVICE_CODE_BOOK_NOT_EXIST, SERVICE_CODE_NOT_FOUND, \
    SERVICE_CODE_CUSTOMER_NOT_EXIST, USER, SERVICE_CODE_USER_PERMISSION
from library.functions import string_to_time, convert_to_int
from library.service.check_active_flag import check_active_flag


class AccountBook(APIView):
    def list_book_account(self, request):
        finished_flag = self.request.query_params.get('finished_flag')
        account_book = BookUser.objects.all()
        if finished_flag:
            account_book = account_book.filter(finished_flag=finished_flag)
        
        now = timezone.now()
        for item in account_book:
            if item.finished_flag is True:
                item.status = 'Đã Trả'
            else:
                if item.date_return <= now:
                    item.status = 'Trễ Hạn'
                else:
                    item.status = 'Chưa Tới Hạn'
            item.save()
        account_book = account_book.annotate(
                book_name=F('book__name'),
                user_name=F('user__name')
        ).values(
                'id',
                'book_id',
                'book_name',
                'user_id',
                'user_name',
                'date_borrow',
                'date_return',
                'finished_flag',
                'status'
        ).order_by('-id')
        self.pagination(account_book)
        return self.response(self.response_paging(self.paging_list))

    def create_book_account(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.POST
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        key_content_list = list(content.keys())
        check_keys_list = ['book_id', 'user_id', 'date_borrow', 'date_return']

        book_id = convert_to_int(content.get('book_id'))
        user_id = convert_to_int(content.get('user_id'))
        date_borrow = content.get('date_borrow')
        date_return = content.get('date_return')

        if not all(key in key_content_list for key in check_keys_list):
            return self.validate_exception(
                'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))

        if date_borrow:
            date_borrow = string_to_time(date_borrow, '%d/%m/%Y %H:%M:%S')
        if date_return:
            date_return = string_to_time(date_return, '%d/%m/%Y %H:%M:%S')
            if date_return < datetime.datetime.now():
                return self.validate_exception("Ngày trả sách phải lớn hơn ngày hiện tại!")
        if date_return < date_borrow:
            return self.response_exception(code=SERVICE_CODE_RECORD_NOT_VALIDATE)
        if check_active_flag(user_id) is True:
            return self.validate_exception("Người dùng không thể mượn thêm sách vì hiện tại đang mượn 3 cuốn sách khác chưa trả lại!")

        book = Book.objects.get(id=book_id, deleted_flag=False)
        if not book:
            return self.response_exception(code=SERVICE_CODE_BOOK_NOT_EXIST)

        book_user = BookUser.objects.create(
            user_id=user_id,
            book_id=book_id,
            date_borrow=date_borrow,
            date_return=date_return
        )

        book.quantity = book.quantity - 1
        book.save()
        return self.response(self.response_success({
            "user_id": book_user.user_id,
            "book_id": book_user.book_id,
            "date_borrow": book_user.date_borrow,
            "date_return": book_user.date_return,
            "status": book_user.status,
            "finished_flag": book_user.finished_flag,
        }))

    def update_book_account(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.POST
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))

        book_user_id = convert_to_int(content.get('book_user_id'))
        finished_flag = content.get('finished_flag')
        if book_user_id:
            try:
                book_user = BookUser.objects.get(id=book_user_id)
            except BookUser.DoesNotExist:
                return self.response_exception(code=SERVICE_CODE_NOT_FOUND)
            if finished_flag is not None:
                book_user.finished_flag = finished_flag
            book_user.save()
            book = Book.objects.get(id=book_user.book_id)
            if book:
                if str(book_user.finished_flag) == 'True':
                    book.quantity = book.quantity + 1
                elif str(book_user.finished_flag) == 'False':
                    book.quantity = book.quantity - 1
                book.save()
            else:
                return self.response_exception(code=SERVICE_CODE_BOOK_NOT_EXIST)
            return self.response(self.response_success({
                "book_user_id": book_user.id,
                "finished_flag": book_user.finished_flag,
            }))
        else:
            return self.validate_exception("Missing book_user_id!")
