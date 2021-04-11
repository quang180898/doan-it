from django.urls import path

from api.backend.v1.author.views import LibraryAuthor

urlpatterns = [
    path('', LibraryAuthor.as_view({'get': 'list_author'})),
    path('create_or_update/', LibraryAuthor.as_view({'post': 'create_or_update'})),
]
