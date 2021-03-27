from django.conf.urls import include
from django.urls import path

from api.backend.v1.login import LoginView
from library.constant.api import URL_BACKEND_API

urlpatterns = [
    path('login/', LoginView.as_view({'post': 'post'})),
    path('log/', include(URL_BACKEND_API + 'log.urls')),
    path('person/', include(URL_BACKEND_API + 'person.urls')),
    path('vehicle/', include(URL_BACKEND_API + 'vehicle.urls')),
    path('user/', include(URL_BACKEND_API + 'user.urls')),
    path('camera/', include(URL_BACKEND_API + 'camera.urls')),
    path('behavior/', include(URL_BACKEND_API + 'behavior.urls')),
    path('account/', include(URL_BACKEND_API + 'account.urls')),
    path('stream/', include(URL_BACKEND_API + 'stream.urls')),
    path('notification/', include(URL_BACKEND_API + 'notification.urls')),
    path('monitor/', include(URL_BACKEND_API + 'monitor.urls')),
    path('setting_notification/', include(URL_BACKEND_API + 'setting.urls')),
    path('setting_vms/', include(URL_BACKEND_API + 'vms.urls')),
    path('setting_group/', include(URL_BACKEND_API + 'group.urls')),
    path('system_location/', include(URL_BACKEND_API + 'system.urls')),
]
