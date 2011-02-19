"""
===============
Django Provider
===============
"""
import ConfigWrapper

class DjangoProvider(object):
    """
    Uses Django's Models to access the database
    """
    def __init__(self):
        c = ConfigWrapper.ConfigWrapper()
        django_where = c.config.get("Django", "installation")
        if django_where not in sys.path:
            sys.path.append(django_where)

        django_name = c.config.get("Django", "app")
        if not 'DJANGO_SETTINGS_MODULE' in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % django_name

    def get_random_user(self):
        """
        Gets a random user from the provider

        :returns: Dictionary
        """
        from provider.models import User
        u = User.objects.order_by('?')[0]
        return {"username": u.username, "password": u.password, "fullname": u.fullname}