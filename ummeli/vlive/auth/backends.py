from django.contrib.auth.backends import RemoteUserBackend

class VodafoneLiveUserBackend(RemoteUserBackend):
    # Automatically create users based
    # on the credentials given
    create_unknown_user = True
