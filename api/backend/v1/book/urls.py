from django.urls import path

from api.backend.v1.book.views import LibraryBook

urlpatterns = [
    path('', LibraryBook.as_view({'get': 'list_book'})),
    path('detail/', LibraryBook.as_view({'get': 'detail_book'})),
    path('create_or_update/', LibraryBook.as_view({'post': 'create_or_update'}))
]
