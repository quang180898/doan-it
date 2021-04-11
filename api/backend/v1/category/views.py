from django.db.models import F

from api.base.apiViews import APIView
from core.postgres.library.category.models import Category
from library.constant.api import (
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_NOT_FOUND,
)
from library.functions import convert_to_int


class LibraryCategory(APIView):
    def list_category(self, request):
        category = Category.objects.all(
        ).annotate(
            category_id=F('id'),
            category_name=F('name'),
            category_description=F('description')
        ).values(
            'category_id',
            'category_name',
            'category_description'
        ).order_by('category_id')
        return self.response(self.response_success(list(category)))

    def create_or_update(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.data
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        category_id = convert_to_int(content.get('category_id'))
        name = content.get('name')
        description = content.get('description')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return self.response_exception(code=SERVICE_CODE_NOT_FOUND)
            category.name = name if name is not None else category.name
            category.description = description if description is not None else category.description
            category.save()
            return self.response(self.response_success({
                "category_id": category.id,
                "category_name": category.name,
                "category_description": category.description
            }))
        else:
            if description is None:
                description = ""
            category = Category.objects.create(
                name=name,
                description=description
            )
            return self.response(self.response_success({
                "category_id": category.id,
                "category_name": category.name,
                "category_description": category.description
            }))
