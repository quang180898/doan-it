import re

from django.db.models import F

from api.base.apiViews import APIView
from core.postgres.library.author.models import Author
from library.constant.api import SERVICE_CODE_NOT_EXISTS_BODY, SERVICE_CODE_BODY_PARSE_ERROR, \
    SERVICE_CODE_FULL_NAME_SPECIAL_CHARACTER, SERVICE_CODE_FULL_NAME_ISSPACE, SERVICE_CODE_MOBILE_ISSPACE, \
    SERVICE_CODE_MOBILE_LENGTH, SERVICE_CODE_MOBILE_DUPLICATE, SERVICE_CODE_MAIL_DUPLICATE, SERVICE_CODE_MAIL_ISSPACE
from library.functions import convert_to_int, is_mobile_valid


class LibraryAuthor(APIView):
    def list_author(self, request):
        author = Author.objects.all(
        ).annotate(
            author_id=F('id'),
            author_name=F('name'),
            author_mail=F('mail'),
            author_mobile=F('mobile')
        ).values(
            'author_id',
            'author_name',
            'author_mail',
            'author_mobile',
        ).order_by('author_id')
        return self.response(self.response_success(list(author)))

    def create_or_update(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.data
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        author_id = convert_to_int(content.get('author_id'))
        name = content.get('name')
        mobile = content.get('mobile')
        mail = content.get('mail')

        if author_id:
            try:
                author = Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                return self.validate_exception("Author không tồn tại!")
            author.name = name if name is not None else author.name
            author.mobile = mobile if mobile is not None else author.mobile
            author.mail = mail if mail is not None else author.mail
            author.save()
            return self.response(self.response_success({
                "author_id": author.id,
                "author_name": author.name,
                "author_mobile": author.mobile,
                "author_mail": author.mail,
            }))
        else:
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if name is not None:
                if regex.search(name) is not None:
                    return self.response_exception(code=SERVICE_CODE_FULL_NAME_SPECIAL_CHARACTER)
                if name.isspace():
                    return self.response_exception(code=SERVICE_CODE_FULL_NAME_ISSPACE)
            else:
                return self.validate_exception("Tên không được để trống!")

            author_new = Author.objects.create(name=name)
            if mobile:
                if Author.objects.filter(mobile=mobile).exists():
                    return self.response_exception(code=SERVICE_CODE_MOBILE_DUPLICATE)
                if mobile.isspace():
                    return self.response_exception(code=SERVICE_CODE_MOBILE_ISSPACE)
                if is_mobile_valid(mobile) is False:
                    return self.response_exception(code=SERVICE_CODE_MOBILE_LENGTH)
                author = Author.objects.get(id=author_new.id)
                author_new.mobile = mobile
                author_new.save()
            if mail is not None:
                if ' ' in mail:
                    return self.validate_exception("Mail không được chứa khoảng trắng!")
                if Author.objects.filter(mail=mail).exists():
                    return self.response_exception(code=SERVICE_CODE_MAIL_DUPLICATE)
                if mail.isspace():
                    return self.response_exception(code=SERVICE_CODE_MAIL_ISSPACE)
                author = Author.objects.get(id=author_new.id)
                author_new.mail = mail
                author_new.save()
            return self.response(self.response_success({
                "author_id": author_new.id,
                "author_name": author_new.name,
                "author_mobile": author_new.mobile,
                "author_mail": author_new.mail,
            }))
