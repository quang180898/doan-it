from django.contrib.auth.hashers import make_password, check_password

from api.base.apiViews import APIView
from core.postgres.library.customer.models import Customer
from library.constant.api import (
    USER_PERMISSION, SERVICE_CODE_NOT_EXISTS_BODY, SERVICE_CODE_BODY_PARSE_ERROR, SERVICE_CODE_CUSTOMER_ERROR
)


class LoginView(APIView):
    def post(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        key_content_list = list(content.keys())
        check_keys_list = ['user_name', 'pass_word']
        user_name = content.get('user_name')
        pass_word = content.get('pass_word')
        if not all(key in key_content_list for key in check_keys_list):
            return self.validate_exception(
                'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))
        customer_login = Customer.objects.filter(
            username=user_name,
            password=check_password(pass_word),
            deleted_flag=False
        ).values(
            'id',
            'name',
            'mail',
            'mobile',
            'address'
        ).first()
        if customer_login:
            return self.response(self.response_success(customer_login))
        else:
            return self.response_exception(code=SERVICE_CODE_CUSTOMER_ERROR)
