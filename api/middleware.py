from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class JWTAuthenticationInMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda:self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        # Already authenticated
        user = get_user(request)
        if user.is_authenticated:
            return user

        # Do JTW authentication
        jwt_authentication = JSONWebTokenAuthentication()

        authenticated = jwt_authentication.authenticate(request)
        if authenticated:
            user, jwt = authenticated

        return user


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class LoggedInUser(Singleton):
    __metaclass__ = Singleton
    request = None
    user = None
    address = None

    def set_data(self, request):
        self.request = id(request)
        if request.user.is_authenticated:
            self.user = request.user
            self.address = request.META.get("REMOTE_ADDR")

    @property
    def current_user(self):
        return self.user

    @property
    def have_user(self):
        return not self.user is None


class LoggedInUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logged_in_user = LoggedInUser()
        logged_in_user.set_data(request)
        response = self.get_response(request)

        return response