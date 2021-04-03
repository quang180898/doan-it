from django.urls import path
from .views import Account

urlpatterns = [
    path('register/', Account.as_view({'post': 'register'})),
    path('info/', Account.as_view({'get': 'info_user'}))
]
