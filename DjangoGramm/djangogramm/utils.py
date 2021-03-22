from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from nanoid import generate


# Create your classes here.
class TokenGenerator(object):
    tokens_storage = list()

    def __init__(self, account):
        self.token = generate(size=40)
        self.account = account

    @classmethod
    def check_token(cls, account, token: str) -> bool:
        for token_obj in cls.tokens_storage:
            if token_obj.token == token and token_obj.account == account:
                cls.tokens_storage.remove(token_obj)
                return True
        return False

    @classmethod
    def make_token(cls, account) -> str:
        obj = TokenGenerator(account)
        cls.tokens_storage.append(obj)
        return obj.token

# Create your decorators here.


def post_method_required(func):
    """Decoraror"""
    def wrapper(request):
        if request.method == 'POST':
            return func(request)
        return HttpResponseNotAllowed(['POST'])
    return wrapper


def confirm_required(func):
    """Decoraror"""
    def wrapper(request, *args, **kwargs):
        if request.user.reg_confirmed_date:
            return func(request, *args, **kwargs)
        return HttpResponseForbidden(
            content=b'You must confirm registration for doing this',
            )
    return wrapper
