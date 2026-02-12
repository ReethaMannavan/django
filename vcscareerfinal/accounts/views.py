from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()  # CustomUser

# -------------------- Registration --------------------


def register_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        errors = {}

        if not username:
            errors['username'] = "Username is required"
        elif User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists"

        if not email:
            errors['email'] = "Email is required"
        elif User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists"

        if not password:
            errors['password'] = "Password is required"

        if errors:
            context['errors'] = errors
            context['username'] = username
            context['email'] = email
        else:
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                subscription_tier='free'
            )
            user.save()

            user = authenticate(request, username=username, password=password)
            login(request, user)

            request.session['registration_success'] = True
            return redirect('home')

    return render(request, 'accounts/register.html', context)



 

# -------------------- Login --------------------
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            context['error'] = "Username and password are required"
        else:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # Redirect ALL users to unified dashboard
                return redirect('dashboard')
            else:
                context['error'] = "Invalid username or password"

    return render(request, 'accounts/login.html', context)


# -------------------- Logout --------------------
def logout_view(request):
    logout(request)
    return redirect('login')




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now
from jobs.models import JobApplication
from consultant.models import ConsultantRequest, MockInterview


@login_required(login_url='login')
def dashboard_view(request):
    user = request.user

    saved_jobs_count = user.saved_jobs.count()


    # Admin Dashboard
    if user.is_staff or user.is_superuser:
       
        requests_qs = ConsultantRequest.objects.select_related("user").all()
        queue_preview = []
        
        for req in requests_qs:
            tier = req.user.subscription_tier
            if tier == "pro_plus":
                sla_hours = 2
                priority = 1
            else:
                sla_hours = 4
                priority = 2
            deadline = req.created_at + timedelta(hours=sla_hours)
            queue_preview.append({
            "req": req,
            "priority": priority,
            "deadline": deadline
        })
        queue_preview.sort(key=lambda x: (x["priority"], x["req"].created_at))
        queue_preview = queue_preview[:5]

    
        return render(request, 'accounts/admin_dashboard.html', {'user': user})

    # ---------------- SUBSCRIPTION EXPIRY CHECK ----------------
    if user.subscription_expiry:
        if user.subscription_expiry and user.subscription_expiry <= now().date():

            if user.pending_downgrade:
                user.subscription_tier = user.pending_downgrade
                user.pending_downgrade = None
                user.subscription_expiry = None
                user.save()

    # ---------------- Application usage tracking ----------------
    month_count = JobApplication.objects.filter(
        candidate=user,
        applied_at__year=now().year,
        applied_at__month=now().month
    ).count()

    if user.subscription_tier == "free":
        limit = 20
    elif user.subscription_tier == "pro":
        limit = 100
    else:
        limit = None

    remaining = None if limit is None else max(limit - month_count, 0)

    # ---------------- Consultant usage tracking ----------------
    consultant_count = ConsultantRequest.objects.filter(
        user=user,
        created_at__year=now().year,
        created_at__month=now().month
    ).count()

    if user.subscription_tier == "pro":
        consultant_limit = 1
    elif user.subscription_tier == "pro_plus":
        consultant_limit = 4
    else:
        consultant_limit = 0

    consultant_remaining = max(consultant_limit - consultant_count, 0)

    # ---------------- Mock interview usage tracking ----------------
    mock_count = MockInterview.objects.filter(
        user=user,
        scheduled_at__year=now().year,
        scheduled_at__month=now().month
    ).count()

    if user.subscription_tier == "pro_plus":
        mock_limit = 4
    else:
        mock_limit = 0

    mock_remaining = max(mock_limit - mock_count, 0)

    return render(request, 'accounts/dashboard.html', {
        'user': user,
        'month_count': month_count,
        'limit': limit,
        'remaining': remaining,
        'consultant_count': consultant_count,
        'consultant_limit': consultant_limit,
        'consultant_remaining': consultant_remaining,

        'mock_count': mock_count,
        'mock_limit': mock_limit,
        'mock_remaining': mock_remaining,
        'saved_jobs_count': saved_jobs_count,
    })






#candidateprofile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CandidateProfile
from .forms import CandidateProfileForm

@login_required
def profile_view(request):
    user = request.user

    # Only Free/Pro users can access
    if user.subscription_tier not in ['free', 'pro', 'pro_plus']:

        messages.error(request, "Your account cannot access this page.")
        return redirect('dashboard')

    profile, created = CandidateProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully saved!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CandidateProfileForm(instance=profile)

    completion = profile.profile_completion()

    return render(request, 'accounts/profile.html', {
        'form': form,
        'completion': completion
    })


#prouser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')
def pro_resume_optimize(request):
    user = request.user
    return render(request, 'accounts/pro_resume_optimize.html', {'user': user})

@login_required(login_url='login')
def pro_job_matching(request):
    user = request.user
    # TODO: add skills-based matching logic
    matched_jobs = []  # placeholder
    return render(request, 'accounts/pro_job_matching.html', {'user': user, 'matched_jobs': matched_jobs})

@login_required(login_url='login')
def pro_courses(request):
    user = request.user
    return render(request, 'accounts/pro_courses.html', {'user': user})

@login_required(login_url='login')
def pro_consultant(request):
    user = request.user
    return render(request, 'accounts/pro_consultant.html', {'user': user})



#placeholder pro
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def pro_feature_placeholder(request):
    if request.user.subscription_tier not in ['pro', 'pro_plus']:

        messages.error(request, "Upgrade to Pro to access this feature.")
        return redirect('dashboard')

    return render(request, 'accounts/pro_placeholder.html')





# from django.contrib.auth import get_user_model
# from django.shortcuts import render, redirect
# from jobs.models import Job, JobApplication, SavedJob

# User = get_user_model()

# def admin_analytics(request):
    
#     if not request.user.is_authenticated or (not request.user.is_superuser and request.user.role != 'admin'):
#         return redirect('dashboard')

#     total_users = User.objects.count()
#     free_users = User.objects.filter(subscription_tier='free').count()
#     pro_users = User.objects.filter(subscription_tier='pro').count()
#     pro_plus_users = User.objects.filter(subscription_tier='pro_plus').count()

#     conversion_rate = round((pro_users / total_users * 100), 1) if total_users else 0

#     total_jobs = Job.objects.count()
#     total_applications = JobApplication.objects.count()
#     total_saved_jobs = SavedJob.objects.count()

#     context = {
#         'total_users': total_users,
#         'free_users': free_users,
#         'pro_users': pro_users,
#         'conversion_rate': conversion_rate,
#         'total_jobs': total_jobs,
#         'total_applications': total_applications,
#         'total_saved_jobs': total_saved_jobs,
#     }
#     return render(request, 'accounts/admin_analytics.html', context)

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.timezone import now

from jobs.models import Job, JobApplication, SavedJob
from consultant.models import ConsultantRequest, MockInterview

User = get_user_model()


def admin_analytics(request):
    if not request.user.is_authenticated or (
        not request.user.is_superuser and request.user.role != "admin"
    ):
        return redirect("dashboard")

    # ---------------- USER METRICS ----------------
    total_users = User.objects.count()
    free_users = User.objects.filter(subscription_tier="free").count()
    pro_users = User.objects.filter(subscription_tier="pro").count()
    pro_plus_users = User.objects.filter(subscription_tier="pro_plus").count()

    conversion_rate = round((pro_users / total_users * 100), 1) if total_users else 0

    # ---------------- JOB METRICS ----------------
    total_jobs = Job.objects.count()
    total_applications = JobApplication.objects.count()
    total_saved_jobs = SavedJob.objects.count()

    # ---------------- MONTHLY USAGE ----------------
    current_month = now().month
    current_year = now().year

    monthly_applications = JobApplication.objects.filter(
        applied_at__month=current_month,
        applied_at__year=current_year
    ).count()

    monthly_mock_interviews = MockInterview.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).count()

    monthly_consultant_sessions = ConsultantRequest.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).count()

    # ---------------- CONSULTANT UTILIZATION ----------------
    total_consultant_requests = ConsultantRequest.objects.count()
    total_mock_interviews = MockInterview.objects.count()

    # ---------------- SLA METRICS ----------------
    completed_requests = ConsultantRequest.objects.filter(status="completed").count()

    sla_compliance = round(
        (completed_requests / total_consultant_requests * 100), 1
    ) if total_consultant_requests else 0

    # ---------------- REVENUE ESTIMATE ----------------
    estimated_revenue = (pro_users * 999) + (pro_plus_users * 29999)

    context = {
        "total_users": total_users,
        "free_users": free_users,
        "pro_users": pro_users,
        "pro_plus_users": pro_plus_users,
        "conversion_rate": conversion_rate,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "total_saved_jobs": total_saved_jobs,
        "monthly_applications": monthly_applications,
        "monthly_mock_interviews": monthly_mock_interviews,
        "monthly_consultant_sessions": monthly_consultant_sessions,
        "total_consultant_requests": total_consultant_requests,
        "total_mock_interviews": total_mock_interviews,
        "sla_compliance": sla_compliance,
        "estimated_revenue": estimated_revenue,
    }

    return render(request, "accounts/admin_analytics.html", context)






#Revised
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta
from .models import Invoice


@login_required
def upgrade_to_pro(request):
    user = request.user

    user.subscription_tier = "pro"
    user.subscription_expiry = timezone.now().date() + timedelta(days=30)
    user.pending_downgrade = None
    user.save()

    Invoice.objects.create(
        user=user,
        plan="Pro",
        amount=999
    )

    messages.success(request, "Upgraded to Pro plan.")
    return redirect("dashboard")



@login_required
def upgrade_to_proplus(request):
    user = request.user

    user.subscription_tier = "pro_plus"
    user.subscription_expiry = timezone.now().date() + timedelta(days=365)
    user.pending_downgrade = None
    user.save()

     # CREATE INVOICE
    Invoice.objects.create(
        user=user,
        plan="Pro Plus",
        amount=29999
    )

    messages.success(request, "Upgraded to Pro Plus plan.")
    return redirect("dashboard")




#downgrade
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def downgrade_free(request):
    request.user.pending_downgrade = "free"
    request.user.save()

    messages.success(request, "Your plan will downgrade at the end of billing cycle.")
    return redirect("subscription")


@login_required
def downgrade_pro(request):
    request.user.pending_downgrade = "pro"
    request.user.save()

    messages.success(request, "Your plan will downgrade at the end of billing cycle.")
    return redirect("subscription")





#subscription
from django.contrib.auth.decorators import login_required
# from django.conf import settings

# @login_required
# def subscription_view(request):
#     return render(request, "accounts/subscription.html")

from django.conf import settings

@login_required
def subscription_view(request):
    return render(request, "accounts/subscription.html", {
        "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID
    })






# ---------------- Resume Optimization ----------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from .models import ResumeOptimization

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))



@login_required
def resume_optimizer(request):
    user = request.user

    if user.subscription_tier == "free":
        messages.error(request, "Resume optimization is available for Pro users.")
        return redirect("subscription")

    month_count = ResumeOptimization.objects.filter(
        user=user,
        created_at__year=now().year,
        created_at__month=now().month
    ).count()

    limit = 3 if user.subscription_tier == "pro" else 20
    remaining = max(limit - month_count, 0)

    ai_result = None
    optimized_resume = None

    if request.method == "POST":

        if month_count >= limit:
            messages.error(request, "Monthly resume optimization quota reached.")
            return redirect("resume-optimizer")

        resume_text = request.POST.get("resume_text")
        job_desc = request.POST.get("job_desc")

        if "resume_file" in request.FILES:
            uploaded_file = request.FILES["resume_file"]
            resume_text = uploaded_file.read().decode("utf-8", errors="ignore")

        if not resume_text:
            messages.error(request, "Please paste or upload a resume.")
            return redirect("resume-optimizer")

        resume_text = resume_text[:3000]
        job_desc = (job_desc or "")[:3000]

        response = groq_client.chat.completions.create(

            messages=[
                {"role": "system", "content": "You are an ATS resume optimization engine."},
                {
                    "role": "user",
                    "content": f"""
Optimize the resume below for ATS compatibility.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Return output in this format:

ATS SCORE:
Give a score out of 100.

MISSING KEYWORDS:
(list)

IMPROVEMENTS:
(list)

OPTIMIZED RESUME:
Write a complete ATS-ready resume using the improved content.
"""
                }
            ],
            model="openai/gpt-oss-20b"
        )

        ai_result = response.choices[0].message.content

        # ✅ Correct extraction
        if ai_result and "OPTIMIZED RESUME" in ai_result:
            optimized_resume = ai_result.split("OPTIMIZED RESUME", 1)[1].strip()

        ResumeOptimization.objects.create(user=user)

        month_count += 1
        remaining = max(limit - month_count, 0)

    return render(request, "accounts/resume_optimizer.html", {
        "month_count": month_count,
        "limit": limit,
        "remaining": remaining,
        "ai_result": ai_result,
        "optimized_resume": optimized_resume,
    })





#pdfresume
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io


def download_optimized_resume_pdf(request):
    data = request.GET.get("data", "")
    username = request.user.username

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="Title",
        fontSize=18,
        spaceAfter=12,
        alignment=1
    )

    section_style = ParagraphStyle(
        name="Section",
        fontSize=12,
        spaceAfter=8,
        spaceBefore=12
    )

    normal_style = styles["Normal"]

    elements = []

    # Header
    elements.append(Paragraph("VCS Careers", title_style))
    elements.append(Paragraph("AI Optimized Resume", section_style))
    elements.append(Paragraph(f"Candidate: {username}", normal_style))
    elements.append(Spacer(1, 20))

    # Resume content
    for line in data.split("\n"):
        elements.append(Paragraph(line, normal_style))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="optimized_resume.pdf"'

    return response




#invoice
from django.contrib.auth.decorators import login_required
from .models import Invoice


@login_required
def billing_history(request):
    invoices = Invoice.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "accounts/billing_history.html", {
        "invoices": invoices
    })


#downloadinvoice
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .utils import generate_invoice_pdf
import os
from django.conf import settings

@login_required
def download_invoice(request, invoice_id):
    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        user=request.user
    )

    relative_path = generate_invoice_pdf(invoice)
    filepath = os.path.join(settings.MEDIA_ROOT, relative_path)

    return FileResponse(open(filepath, "rb"), as_attachment=True)





#razorpay
import razorpay
from django.conf import settings
from django.http import JsonResponse

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)



@login_required
def create_payment_order(request, plan):
    if plan == "pro":
        amount = 99900
    else:
        amount = 2999900

    order = razorpay_client.order.create({

        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    return JsonResponse(order)



import json

@login_required
def verify_payment(request):
    data = json.loads(request.body)

    params_dict = {
        'razorpay_order_id': data.get('razorpay_order_id'),
        'razorpay_payment_id': data.get('razorpay_payment_id'),
        'razorpay_signature': data.get('razorpay_signature')
    }

    try:
        razorpay_client.utility.verify_payment_signature(params_dict)


        plan = data.get("plan")

        if plan == "pro":
            return upgrade_to_pro(request)
        else:
            return upgrade_to_proplus(request)

    except:
        messages.error(request, "Payment verification failed.")
        return redirect("subscription")


