from django.urls import path

from api.backend.v1.category.views import LibraryCategory

urlpatterns = [
    path('', LibraryCategory.as_view({'get': 'list_category'})),
    path('create_or_update/', LibraryCategory.as_view({'post': 'create_or_update'})),
]
