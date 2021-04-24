from django.urls import path

from api.backend.v1.book.views import LibraryBook

urlpatterns = [
    path('', LibraryBook.as_view({'get': 'list_book'})),
    path('detail/', LibraryBook.as_view({'get': 'detail_book'})),
    path('same_category/', LibraryBook.as_view({'get': 'book_same_category'})),
    path('delete/', LibraryBook.as_view({'post': 'delete_book'})),
    path('create_or_update/', LibraryBook.as_view({'post': 'create_or_update'}))
]
