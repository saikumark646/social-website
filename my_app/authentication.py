# """
#     • authenticate(): It takes the request object and user credentials as
# parameters. It has to return a user object that matches those credentials
# if the credentials are valid, or None otherwise. The request parameter is
# an HttpRequest object, or None if it's not provided to authenticate().

# • get_user(): This takes a user ID parameter and has to return a user object.
#    """


from django.contrib.auth.models import User

# Authenticate using an e-mail address.


class EmailAuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
