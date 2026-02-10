from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Job, JobApplication
from accounts.models import CustomUser
from django.contrib import messages


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from datetime import timedelta
from django.utils import timezone


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Job

# ---------------- Admin Mixin ----------------
class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or request.user.is_staff):

            messages.error(request, "Admin access only.")
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

# ---------------- Admin Job List ----------------
class AdminJobListView(AdminRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/admin_job_list.html'
    context_object_name = 'jobs'
    ordering = ['-posted_at']

# ---------------- Admin Job Create ----------------
class AdminJobCreateView(AdminRequiredMixin, CreateView):
    model = Job
    fields = '__all__'
    template_name = 'jobs/admin_job_form.html'
    success_url = reverse_lazy('admin-job-list')

# ---------------- Admin Job Update ----------------
class AdminJobUpdateView(AdminRequiredMixin, UpdateView):
    model = Job
    fields = '__all__'
    template_name = 'jobs/admin_job_form.html'
    success_url = reverse_lazy('admin-job-list')

# ---------------- Admin Job Delete ----------------
class AdminJobDeleteView(AdminRequiredMixin, DeleteView):
    model = Job
    template_name = 'jobs/admin_job_confirm_delete.html'
    success_url = reverse_lazy('admin-job-list')



from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import JobApplication
from django.contrib import messages
from django.views import View

from django.core.mail import send_mail
from django.conf import settings

class AdminApplicationListView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login'

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff


    def handle_no_permission(self):
        messages.error(self.request, "Admin access only.")
        return redirect('dashboard')

    def get(self, request):
        applications = JobApplication.objects.select_related('job', 'candidate').all().order_by('-applied_at')
        # (filters and pagination code remains unchanged)
        paginator = Paginator(applications, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'jobs/admin_applications_list.html', {
            'applications': page_obj,
            'page_obj': page_obj
        })

    def post(self, request):
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')

        if application_id and new_status:
            try:
                app = JobApplication.objects.get(id=application_id)
                app.status = new_status
                app.save()

                # --- SEND EMAIL NOTIFICATION ---
                candidate = app.candidate
                candidate_email = candidate.email
                job_title = app.job.title

                # Build email subject & message
                if new_status == 'shortlisted':
                    subject = f"Your Application Status for {job_title}"
                    message = (
                        f"Hello {candidate.username},\n\n"
                        f"Good news! Your application for the job '{job_title}' has been *shortlisted* by the admin.\n\n"
                        "We will contact you soon with next steps.\n\n"
                        "Best regards,\n"
                        "The Team"
                    )
                elif new_status == 'rejected':
                    subject = f"Your Application Status for {job_title}"
                    message = (
                        f"Hello {candidate.username},\n\n"
                        f"Thank you for applying for '{job_title}'. "
                        "Unfortunately, your application has not been selected at this time.\n\n"
                        "We appreciate your interest and wish you good luck!\n\n"
                        "Best regards,\n"
                        "The Team"
                    )
                else:
                    subject = None
                    message = None

                # Actually send email
                if subject and message and candidate_email:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [candidate_email],
                        fail_silently=False
                    )

            except JobApplication.DoesNotExist:
                messages.error(request, "Application not found.")

        return redirect('admin-applications')


#candidatejobs
class JobListView(View):
    def get(self, request):
        jobs = Job.objects.all().order_by('-posted_at')

        # ---------------- Filters ----------------
        query = request.GET.get('q')
        location = request.GET.get('location')
        job_type = request.GET.get('job_type')

        if query:
            jobs = jobs.filter(title__icontains=query)
        if location:
            jobs = jobs.filter(location__icontains=location)
        if job_type:
            jobs = jobs.filter(job_type=job_type)

        # ---------------- Track user applications ----------------
        user_applications = {}
        user_saved_jobs = []

        if request.user.is_authenticated:
            # Applications
            user_applications = {app.job.id: app.status for app in request.user.applications.all()}
            # Saved jobs (assuming ManyToManyField saved_jobs in CustomUser)
            if hasattr(request.user, 'saved_jobs'):
                user_saved_jobs = list(request.user.saved_jobs.values_list('id', flat=True))

        # ---------------- Pagination ----------------
        paginator = Paginator(jobs, 6)  # 6 jobs per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # ---------------- NEW badge logic ----------------
        now = timezone.now()
        jobs_with_new = []
        for job in page_obj:
            is_new = (now - job.posted_at) <= timedelta(days=3)
            jobs_with_new.append((job, is_new))

        context = {
            'jobs_with_new': jobs_with_new,
            'page_obj': page_obj,
            'user_applications': user_applications,
            'user_saved_jobs': user_saved_jobs,
        }
        return render(request, 'jobs/job_list.html', context)


# ---------------- Job Detail ----------------
class JobDetailView(View):
    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        has_applied = False
        application_status = None
        is_saved = False

        if request.user.is_authenticated:
            application = JobApplication.objects.filter(
                job=job,
                candidate=request.user
            ).first()

            if application:
                has_applied = True
                application_status = application.status

            if hasattr(request.user, 'saved_jobs'):
                is_saved = request.user.saved_jobs.filter(id=job.id).exists()

        context = {
            'job': job,
            'has_applied': has_applied,
            'application_status': application_status,
            'is_saved': is_saved,
        }
        return render(request, 'jobs/job_detail.html', context)


# ---------------- Apply Job ----------------
# class ApplyJobView(View):
#     def get(self, request, pk):
#         job = get_object_or_404(Job, pk=pk)
#         return render(request, 'jobs/job_apply.html', {'job': job})

#     def post(self, request, pk):
#         job = get_object_or_404(Job, pk=pk)
#         resume = request.FILES.get('resume')
#         if not resume:
#             messages.error(request, "Please upload a resume to apply.")
#             return redirect('job-apply', pk=pk)

#         JobApplication.objects.create(
#             job=job,
#             candidate=request.user,
#             resume=resume
#         )
#         messages.success(request, "Application submitted successfully!")
#         return redirect('job-list')



from django.utils.timezone import now

class ApplyJobView(View):
    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        return render(request, 'jobs/job_apply.html', {'job': job})

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        resume = request.FILES.get('resume')

        if not resume:
            messages.error(request, "Please upload a resume to apply.")
            return redirect('job-apply', pk=pk)

        user = request.user

        if JobApplication.objects.filter(job=job, candidate=user).exists():
            messages.warning(request, "You already applied for this job.")
            return redirect("job-detail", pk=pk)

        # ---------------- Subscription Quota Check ----------------
        if user.subscription_tier == "free":
            limit = 20
        elif user.subscription_tier == "pro":
            limit = 100
        else:
            limit = None  # pro_plus = unlimited

        if limit is not None:
            monthly_count = JobApplication.objects.filter(
                candidate=user,
                applied_at__year=now().year,
                applied_at__month=now().month
            ).count()

            if monthly_count >= limit:
                messages.error(
                    request,
                    "You’ve reached your monthly application limit. Upgrade your plan."
                )
                return redirect('subscription')

        # ---------------- Create Application ----------------
        JobApplication.objects.create(
            job=job,
            candidate=user,
            resume=resume
        )

        messages.success(request, "Application submitted successfully!")
        return redirect('job-list')




# ---------------- Saved Jobs Placeholder ----------------
# jobs/views.py
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render

@method_decorator(login_required, name='dispatch')
class SavedJobsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Get full Job objects, not just IDs
        saved_jobs = request.user.saved_jobs.all()
        
        context = {
            'saved_jobs': saved_jobs,
        }
        return render(request, 'jobs/saved_jobs.html', context)







#savedjobs
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Job, SavedJob
from django.core.paginator import Paginator


@login_required
def save_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    SavedJob.objects.get_or_create(user=request.user, job=job)
    return redirect('job-list')

@login_required
def unsave_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    SavedJob.objects.filter(user=request.user, job=job).delete()
    return redirect('job-list')

@method_decorator(login_required, name='dispatch')
class SavedJobsView(View):
    def get(self, request):
        saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
        return render(request, 'jobs/saved_jobs.html', {
            'saved_jobs': saved_jobs
        })



#Prouser
# jobs/views.py
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from accounts.models import CandidateProfile
from .models import Job

@method_decorator(login_required, name='dispatch')
class ProJobMatchingView(View):
    def get(self, request):
        user = request.user

        # 🚫 Block free users
        if user.subscription_tier not in ['pro', 'pro_plus']:

            return render(request, 'jobs/pro_upgrade_required.html')

        try:
            profile = CandidateProfile.objects.get(user=user)
        except CandidateProfile.DoesNotExist:
            return render(request, 'jobs/pro_no_profile.html')

        if not profile.skills:
            return render(request, 'jobs/pro_no_skills.html')

        user_skills = set(
            s.strip().lower()
            for s in profile.skills.split(',')
            if s.strip()
        )

        matched_jobs = []

        for job in Job.objects.exclude(skills__isnull=True).exclude(skills=''):
            job_skills = set(
                s.strip().lower()
                for s in job.skills.split(',')
                if s.strip()
            )

            if not job_skills:
                continue

            matched = user_skills.intersection(job_skills)
            match_percentage = int((len(matched) / len(job_skills)) * 100)

            if match_percentage > 0:
                matched_jobs.append({
                    'job': job,
                    'match_percentage': match_percentage,
                    'matched_skills': matched
                })

        matched_jobs.sort(
            key=lambda x: x['match_percentage'],
            reverse=True
        )

        return render(request, 'jobs/pro_job_matching.html', {
            'matched_jobs': matched_jobs
        })



#AICHATBOT
# AICHATBOT
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from .models import ChatbotUsage

from groq import Groq

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)



@login_required
def pro_interview_chatbot(request):
    if request.user.subscription_tier == "free":
        return redirect("subscription")

    user = request.user

    chatbot_count = ChatbotUsage.objects.filter(
        user=user,
        created_at__year=now().year,
        created_at__month=now().month
    ).count()

    if user.subscription_tier == "pro":
        chatbot_limit = 250
    else:
        chatbot_limit = None  # Pro Plus unlimited

    chatbot_remaining = (
        None if chatbot_limit is None else max(chatbot_limit - chatbot_count, 0)
    )

    return render(request, 'jobs/pro_interview_chatbot.html', {
        "chatbot_count": chatbot_count,
        "chatbot_limit": chatbot_limit,
        "chatbot_remaining": chatbot_remaining,
    })



@login_required
def pro_interview_chatbot_api(request):
    if request.method == "POST":
        user = request.user

        # Block Free users
        if user.subscription_tier == "free":
            return JsonResponse({"answer": "AI chatbot is available for Pro users only."})

        # -------- Monthly usage tracking --------
        monthly_count = ChatbotUsage.objects.filter(
            user=user,
            created_at__year=now().year,
            created_at__month=now().month
        ).count()

        if user.subscription_tier == "pro":
            limit = 250
        else:
            limit = None  # Pro Plus unlimited

        if limit is not None and monthly_count >= limit:
            return JsonResponse({
                "answer": "You’ve reached your monthly chatbot limit (250)."
            })

        user_message = request.POST.get('message', '')

        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful AI interviewer."},
                    {"role": "user", "content": user_message}
                ],
                model="openai/gpt-oss-20b"
            )

            answer = response.choices[0].message.content

            # Track usage
            ChatbotUsage.objects.create(user=user)

        except Exception:
            answer = "Sorry, I couldn't generate a response."

        return JsonResponse({"answer": answer})

    return JsonResponse({"error": "Invalid request"}, status=400)





from django.shortcuts import redirect
from django.contrib import messages
from .models import NewsletterSubscriber

def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")

        NewsletterSubscriber.objects.get_or_create(email=email)

        messages.success(request, "You have subscribed successfully!")

    return redirect(request.META.get("HTTP_REFERER", "/"))

