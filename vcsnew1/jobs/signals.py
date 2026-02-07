from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Job, NewsletterSubscriber

@receiver(post_save, sender=Job)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = NewsletterSubscriber.objects.values_list("email", flat=True)

        if subscribers:
            send_mail(
                subject=f"New Job Posted: {instance.title}",
                message = f"""
New job posted on VCS Careers!

Title: {instance.title}

Visit the platform to apply.
"""
,
                from_email=None,
                recipient_list=list(subscribers),
                fail_silently=True,
            )
