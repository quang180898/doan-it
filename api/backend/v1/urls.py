from django.conf.urls import include
from django.urls import path

from api.backend.v1.login import LoginView
from library.constant.api import URL_BACKEND_API

urlpatterns = [
    path('login/', LoginView.as_view({'post': 'post'})),
    path('account/', include(URL_BACKEND_API + 'account.urls'))
]
