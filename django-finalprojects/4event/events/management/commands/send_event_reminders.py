from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from events.models import Event
from datetime import timedelta
from django.core.mail import send_mail

class Command(BaseCommand):
    help = "Send email reminders to registered users for events happening in N days (default: 1 day)."

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=1, help='Days ahead to remind (default 1)')

    def handle(self, *args, **options):
        days = options['days']
        now = timezone.now()
        start = now + timedelta(days=days)
        end = start + timedelta(days=1)
        events = Event.objects.filter(date__gte=start, date__lt=end)
        sent = 0
        for event in events:
            regs = event.registrations.filter(status='REGISTERED').select_related('user')
            for r in regs:
                try:
                    send_mail(
                        subject=f"Reminder: {event.title} on {event.date.strftime('%Y-%m-%d %H:%M')}",
                        message=f"Hi {r.user.username},\n\nThis is a reminder for {event.title} happening on {event.date}.\n\n",
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                        recipient_list=[r.user.email],
                        fail_silently=True,
                    )
                    sent += 1
                except Exception:
                    pass
        self.stdout.write(self.style.SUCCESS(f"Reminders sent: {sent}"))
