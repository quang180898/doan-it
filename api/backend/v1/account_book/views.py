import datetime

from api.base.apiViews import APIView
from core.postgres.library.book.models import BookUser
from core.postgres.library.customer.models import Customer
from library.constant.api import SERVICE_CODE_NOT_EXISTS_BODY, SERVICE_CODE_BODY_PARSE_ERROR, \
    SERVICE_CODE_RECORD_NOT_VALIDATE, SERVICE_CODE_NOT_EXISTS_USER
from library.functions import string_to_time


class AccountBook(APIView):
    def list_book_account(self, request):
        finished_flag = self.request.query_params.get('finished_flag')
        account_book = BookUser.objects.all()
        if finished_flag:
            account_book = account_book.filter(finished_flag=finished_flag)
        account_book = account_book.values(
            'id',
            'book_id',
            'user_id',
            'date_borrow',
            'date_return',
            'finished_flag',
            'status'
        ).order_by('-date_borrow')
        self.pagination(account_book)
        return self.response(self.response_paging(self.paging_list))

    def create_or_update(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.POST
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))

        book_id = content.get('book_id')
        user_id = content.get('user_id')
        date_borrow = content.get('date_borrow')
        date_return = content.get('date_return')

        if date_borrow:
            date_borrow = string_to_time(date_borrow, '%d/%m/%Y %H:%M:%S')
        if date_return:
            date_return = string_to_time(date_return, '%d/%m/%Y %H:%M:%S')

        if date_return < date_borrow:
            return self.response_exception(code=SERVICE_CODE_RECORD_NOT_VALIDATE)
        user = Customer.objects.get(id=user_id, deleted_flag=False)
        if user:
            if user.active_flag is False:
                return self.validate_exception("Người dùng không thể mượn thêm sách vì hiện tại đang mượn 3 cuốn sách khác chưa trả lại!")
        else:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_USER)
