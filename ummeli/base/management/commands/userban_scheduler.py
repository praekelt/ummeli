from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Ban/Unban users'

    def handle(self, **options):
        from datetime import datetime
        from django.contrib.auth.models import User
        from django.db.models import Q
        from ummeli.base.models import UserBan

        now = datetime.now()

        # Must be banned permanently
        q1 = Q(ban_on__lte=now, unban_on__isnull=True)
        # Must remain banned till unban date
        q2 = Q(ban_on__lte=now, unban_on__gt=now)

        # Ban users
        users_pk = UserBan.objects.filter(q1 | q2).values_list(
            'user', flat=True)
        User.objects.filter(pk__in=users_pk).update(is_active=False)

        # Unban users
        users = UserBan.objects.filter(
            is_unbanned=False, unban_on__lte=now)
        users_pk = users.values_list('user', flat=True)
        User.objects.filter(pk__in=users_pk).update(is_active=True)
        users.update(is_unbanned=True)
