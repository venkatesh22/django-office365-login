"""Glue between OpenID and django.contrib.auth."""
from models import UserOffice365ID
__metaclass__ = type
from django.contrib.auth.models import User
import conf

class Office365AuthBackend:
    """A django.contrib.auth backend that authenticates the user based on
    an office365 response."""

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, **kwargs):
        user_details = kwargs.get('user_details')
        if user_details is None:
            return None
        user = None
        try:
            user_openid = UserOffice365ID.objects.get(
                office365_id__exact=self._get_user_id(user_details))
        except UserOffice365ID.DoesNotExist:
            if conf.CREATE_USERS:
                user = self.create_user_from_office365(user_details)
        else:
            user = user_openid.user

        if user is None:
            return None

        details = self._extract_user_details(user_details)
        if details:
            self.update_user_details(user, details)

        return user

    def _get_user_id(self, user_details):
        return user_details.get('oid')
    
    def _extract_user_details(self, user_details):
        first_name = user_details.get('name')
        last_name = ""
        email = user_details.get('preferred_username')
        return dict(email=email,
                    first_name=first_name, last_name=last_name)

    def create_user_from_office365(self, user_details):
        details = self._extract_user_details(user_details)
        nickname = details.get('nickname') or 'openiduser'
        email = details['email'] or ''

        # Pick a username for the user based on their nickname,
        # checking for conflicts.
        i = 1
        while True:
            username = nickname
            if i > 1:
                username += str(i)
            try:
                User.objects.get(username__exact=username)
            except User.DoesNotExist:
                break
            i += 1

        user = User.objects.create_user(username, email, password=None)
        self.update_user_details(user, details)
        UserOffice365ID.objects.create(
                office365_id=self._get_user_id(user_details), user=user)
        return user

    def update_user_details(self, user, details):
        updated = False
        if details['first_name']:
            user.first_name = details['first_name']
            updated = True
        if details['last_name']:
            user.last_name = details['last_name']
            updated = True
        if details['email']:
            user.email = details['email']
            updated = True

        if updated:
            user.save()

