from django.conf import settings

CREATE_USERS = getattr(
    settings, 'CREATE_USERS', True)

OFFICE365_CLIENT_ID = getattr(
    settings, 'OFFICE365_CLIENT_ID', None)

OFFICE365_CLIENT_SECRET = getattr(
    settings, 'OFFICE365_CLIENT_SECRET', None)

OFFICE365_REDIRECT_URI = getattr(
    settings, 'OFFICE365_REDIRECT_URI', None)

AUTHORITY = getattr(
    settings, 'AUTHORITY', "https://login.microsoftonline.com/common")

USER_ENDPOINT = getattr(
    settings, 'USER_ENDPOINT', "https://graph.microsoft.com/v1.0/users")

SCOPES = getattr(
    settings, 'USER_ENDPOINT', ["User.ReadBasic.All"])
