from django.db import models
from django.conf import settings

JOB_TYPE_CHOICES = (
    ('fulltime', 'Full-Time'),
    ('parttime', 'Part-Time'),
    ('internship', 'Internship'),
    ('contract', 'Contract'),
)

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    experience = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='fulltime')
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')  # Admin/Consultant
    skills = models.TextField(
        blank=True,
        null=True,
        help_text="Comma-separated skills (e.g. Python, Django, SQL)"
    )

    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='applications/resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    status_choices = (
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=50, choices=status_choices, default='applied')

    def __str__(self):
        return f"{self.candidate.username} applied for {self.job.title}"





from django.db import models
from django.conf import settings

class SavedJob(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_jobs'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='saved_by'
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"





#newsletter
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



#chatbotusage
from django.conf import settings
from django.db import models

class ChatbotUsage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chatbot_usage"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
