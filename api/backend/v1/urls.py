from django.conf.urls import include
from django.urls import path

from api.backend.v1.login import LoginView
from library.constant.api import URL_BACKEND_API

urlpatterns = [
    path('login/', LoginView.as_view({'post': 'post'})),
    path('account/', include(URL_BACKEND_API + 'account.urls')),
    path('book/', include(URL_BACKEND_API + 'book.urls')),
    path('category/', include(URL_BACKEND_API + 'category.urls')),
    path('author/', include(URL_BACKEND_API + 'author.urls')),
    path('publishing_company/', include(URL_BACKEND_API + 'publishing_company.urls')),
    path('account_book/', include(URL_BACKEND_API + 'account_book.urls'))
]
