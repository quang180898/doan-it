from django.urls import path

from api.backend.v1.publishing_company.views import LibraryPublishingCompany

urlpatterns = [
    path('', LibraryPublishingCompany.as_view({'get': 'list_publishing_company'})),
    path('create_or_update/', LibraryPublishingCompany.as_view({'post': 'create_or_update'})),
]
