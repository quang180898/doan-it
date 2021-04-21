from django.urls import path
from .views import AccountBook

urlpatterns = [
    path('', AccountBook.as_view({'get': 'list_book_account'})),
    path('create/', AccountBook.as_view({'post': 'create_book_account'})),
    path('update/', AccountBook.as_view({'post': 'update_book_account'})),
]
