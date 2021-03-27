from api.base.apiViews import APIView
from api.base.authentication import BasicAuthentication
from library.constant.api import (
    USER_PERMISSION
)
from library.constant.services import DEVICE_SIGN_UP
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

        context = {
            'user_id': user.id,
            'permission_id': user.permission_id,
            'permission_name': USER_PERMISSION.get(user.permission_id),
            'full_name': user.name,
            'token': user.get_key,
            'username': user.username,
            'mobile': user.mobile,
            'device_notification': notify_flag,
        }

        return self.response(self.response_success(context))


