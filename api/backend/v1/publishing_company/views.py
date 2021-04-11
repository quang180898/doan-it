from django.db.models import F

from api.base.apiViews import APIView
from core.postgres.library.category.models import Category
from core.postgres.library.publishing_company.models import PublishingCompany
from library.constant.api import (
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_NOT_FOUND,
)
from library.functions import convert_to_int


class LibraryPublishingCompany(APIView):
    def list_publishing_company(self, request):
        publishing_company = PublishingCompany.objects.all(
        ).annotate(
            publishing_company_id=F('id'),
            publishing_company_name=F('name'),
            publishing_company_mobile=F('mobile'),
            publishing_company_mail=F('mail'),
            publishing_company_address=F('address'),
            publishing_company_description=F('description')
        ).values(
            'publishing_company_id',
            'publishing_company_name',
            'publishing_company_mobile',
            'publishing_company_mail',
            'publishing_company_address',
            'publishing_company_description'
        ).order_by('publishing_company_id')
        return self.response(self.response_success(list(publishing_company)))

    def create_or_update(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.data
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        key_content_list = list(content.keys())
        check_keys_list = ['name', 'mobile', 'address']
        publishing_company_id = convert_to_int(content.get('publishing_company_id'))
        name = content.get('name')
        mobile = content.get('mobile')
        mail = content.get('mail')
        fax = content.get('fax')
        website = content.get('website')
        address = content.get('address')
        description = content.get('description')
        if publishing_company_id:
            try:
                publishing_company = PublishingCompany.objects.get(id=publishing_company_id)
            except PublishingCompany.DoesNotExist:
                return self.response_exception(code=SERVICE_CODE_NOT_FOUND)
            publishing_company.name = name if name is not None else publishing_company.name
            publishing_company.mobile = mobile if mobile is not None else publishing_company.mobile
            publishing_company.mail = mail if mail is not None else publishing_company.mail
            publishing_company.address = address if address is not None else publishing_company.address
            publishing_company.fax = fax if fax is not None else publishing_company.fax
            publishing_company.website = website if website is not None else publishing_company.website
            publishing_company.description = description if description is not None else publishing_company.description
            publishing_company.save()
            return self.response(self.response_success({
                "publishing_company_id": publishing_company.id,
                "publishing_company_name": publishing_company.name,
                "publishing_company_mobile": publishing_company.mobile,
                "publishing_company_mail": publishing_company.mail,
                "publishing_company_address": publishing_company.address,
                "publishing_company_fax": publishing_company.fax,
                "publishing_company_website": publishing_company.website,
                "publishing_company_description": publishing_company.description
            }))
        else:
            if not all(key in key_content_list for key in check_keys_list):
                return self.validate_exception(
                    'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))

            if description is None:
                description = ""
            if fax is None:
                fax = ""
            if website is None:
                website = ""
            publishing_company = PublishingCompany.objects.create(
                name=name,
                mobile=mobile,
                mail=mail,
                address=address,
                fax=fax,
                website=website,
                description=description
            )
            return self.response(self.response_success({
                "publishing_company_id": publishing_company.id,
                "publishing_company_name": publishing_company.name,
                "publishing_company_mobile": publishing_company.mobile,
                "publishing_company_mail": publishing_company.mail,
                "publishing_company_address": publishing_company.address,
                "publishing_company_fax": publishing_company.fax,
                "publishing_company_website": publishing_company.website,
                "publishing_company_description": publishing_company.description
            }))
