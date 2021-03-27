from django.urls import path

from .views import Account

urlpatterns = [
    path('list/', Account.as_view({'get': 'list_user'})),
    path('info/', Account.as_view({'get': 'info_user'})),
    path('create_or_update/', Account.as_view({'post': 'create_or_update'})),
    path('list_vms/', Account.as_view({'get': 'vms_of_admin'})),
    path('change_status/', Account.as_view({'post': 'set_status'})),
    path('delete/', Account.as_view({'post': 'delete'})),
]
