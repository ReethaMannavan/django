from django.core.management.base import BaseCommand
from django.utils.timezone import now
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Process subscription expiries and downgrades"

    def handle(self, *args, **kwargs):
        today = now().date()

        users = CustomUser.objects.filter(subscription_expiry__lte=today)

        for user in users:
            if user.pending_downgrade:
                user.subscription_tier = user.pending_downgrade
                user.pending_downgrade = None
                user.subscription_expiry = None
                user.save()

                self.stdout.write(
                    f"Downgraded {user.username} to {user.subscription_tier}"
                )
