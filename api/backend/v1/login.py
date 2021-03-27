from django.db.models import F
from django.utils import translation

from api.base.apiViews import APIView
from api.base.authentication import BasicAuthentication
from cctv_config.root_local import CHATTING_SERVER, CLOUD_SERVER_URL, RABBIT_NOTIFICATION_INFO
from core.postgres.customer.models import Customer
from library.constant.api import (
    SERVICE_CODE_CUSTOMER_NOT_EXIST,
    USER_PERMISSION
)
from library.constant.services import DEVICE_SIGN_UP, HOST_VIDEO_CALL
from library.service.functions import CHATTING_SERVICE_HEAR, request_api
from library.service.service_urls import SERVICE_CHATTING_LOGIN_URL
from library.services import send_post_message


class LoginView(APIView):
    # setting user/password authentication.
    authentication_classes = (BasicAuthentication,)
    permission_classes = ()

    def post(self, request):
        user = request.user
        notify_flag = False
        device_token = request.data.get('device_token')
        if device_token:
            device = {'user_id': user.id, 'device_token': device_token}
            response = send_post_message(DEVICE_SIGN_UP, device)
            notify_flag = True if response['success'] else False

        if user.avatar_url is not None and user.avatar_url != "":
            avatar_url = CLOUD_SERVER_URL + user.avatar_url
        else:
            avatar_url = ""
        # status_code, data = request_api(CHATTING_SERVER + SERVICE_CHATTING_LOGIN_URL, method='post',
        #                                 headers=CHATTING_SERVICE_HEAR,
        #                                 content={
        #                                     'system_user_id': user.id
        #                                 })
        # data = self.decode_to_json(data)
        customer_permission_code = Customer.objects.filter(
            id=self.user.id,
            deleted_flag=False
        ).values(
            'permission__code'
        ).first()
        if not customer_permission_code:
            return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
        context = {
            'user_id': user.id,
            'permission_id': user.permission_id,
            'permission_name': USER_PERMISSION.get(user.permission_id),
            'permission_code': customer_permission_code['permission__code'],
            'full_name': user.name,
            'token': user.get_key,
            'avatar_url': avatar_url,
            'username': user.username,
            'mobile': user.mobile,
            'device_notification': notify_flag,
            'rabbit_notification': {
                'rabbit_user': RABBIT_NOTIFICATION_INFO['RABBIT_USER'],
                'rabbit_pass': RABBIT_NOTIFICATION_INFO['RABBIT_PASS'],
                'rabbit_host': RABBIT_NOTIFICATION_INFO['RABBIT_HOST'],
                'rabbit_port_wss': RABBIT_NOTIFICATION_INFO['RABBIT_PORT_WSS'],
                'rabbit_vhot': RABBIT_NOTIFICATION_INFO['RABBIT_VHOT'],
                'rabbit_exchange_topic': RABBIT_NOTIFICATION_INFO['RABBIT_EXCHANGE_TOPIC']
            }
            # 'chat_info': {
            #     'api_token': data['detail']['api_token'],
            #     'queue_token': data['detail']['queue_token'],
            #     'rabbit_info': data['detail']['rabbit_info']
            # }
        }

        return self.response(self.response_success(context))


