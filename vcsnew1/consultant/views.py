from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ConsultantRequest
from django.contrib import messages
from django.utils.timezone import now

@login_required
def request_consultant(request):
    user = request.user

    if user.subscription_tier not in ['pro', 'pro_plus']:
        return redirect('subscription')

    # -------- Monthly consultant quota --------
    if user.subscription_tier == "pro":
        limit = 1
    else:
        limit = 4

    monthly_count = ConsultantRequest.objects.filter(
        user=user,
        created_at__year=now().year,
        created_at__month=now().month
    ).count()

    if monthly_count >= limit:
        messages.error(request, "You’ve reached your monthly consultant session limit.")
        return redirect('dashboard')

    # ------------------------------------------

    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        message = request.POST.get('message')

        ConsultantRequest.objects.create(
            user=user,
            purpose=purpose,
            message=message
        )
        messages.success(request, "Consultant session requested successfully.")
        return redirect('dashboard')

    return render(request, 'consultant/request_consultant.html')






from django.contrib.auth.decorators import login_required
from .models import ConsultantRequest

@login_required
def my_consultant_requests(request):
    requests = ConsultantRequest.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'requests': requests,
        'total_requests': requests.count(),
        'pending_count': requests.filter(status='pending').count(),
        'in_progress_count': requests.filter(status='in_progress').count(),
        'completed_count': requests.filter(status='completed').count(),
    }

    return render(request, 'consultant/my_requests.html', context)




# from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import redirect
# from .models import ConsultantRequest

# @staff_member_required
# def admin_consultant_requests(request):
#     requests = ConsultantRequest.objects.all().order_by('-created_at')

#     if request.method == 'POST':
#         req_id = request.POST.get('request_id')
#         new_status = request.POST.get('status')
#         ConsultantRequest.objects.filter(id=req_id).update(status=new_status)
#         return redirect('admin-consultant-requests')

#     return render(request, 'consultant/admin_requests.html', {
#         'requests': requests
#     })


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.utils.timezone import now
from datetime import timedelta
from .models import ConsultantRequest


@staff_member_required
def admin_consultant_requests(request):

    requests_qs = ConsultantRequest.objects.select_related("user").all()

    enriched_requests = []

    for req in requests_qs:
        tier = req.user.subscription_tier

        # SLA rules (from BRD)
        if tier == "pro_plus":
            sla_hours = 2
            priority = 1
        else:
            sla_hours = 4
            priority = 2

        deadline = req.created_at + timedelta(hours=sla_hours)
        remaining_time = deadline - now()

        if remaining_time.total_seconds() <= 0:
            sla_status = "overdue"
        elif remaining_time <= timedelta(hours=1):
            sla_status = "warning"
        else:
            sla_status = "ok"

        enriched_requests.append({
            "req": req,
            "sla_status": sla_status,
            "priority": priority,
            "deadline": deadline
        })

    # ---------------- PRIORITY SORT ----------------
    enriched_requests.sort(key=lambda x: (x["priority"], x["req"].created_at))

    if request.method == "POST":
        req_id = request.POST.get("request_id")
        new_status = request.POST.get("status")
        ConsultantRequest.objects.filter(id=req_id).update(status=new_status)
        return redirect("admin-consultant-requests")

    return render(request, "consultant/admin_requests.html", {
        "requests": enriched_requests
    })


#mockinterview
from django.utils.timezone import now
from django.contrib import messages
from .models import MockInterview


from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive

@login_required
def schedule_mock_interview(request):
    user = request.user

    if user.subscription_tier != "pro_plus":
        messages.error(request, "Mock interviews are available only for Pro Plus users.")
        return redirect("subscription")

    limit = 4

    monthly_count = MockInterview.objects.filter(
        user=user,
        created_at__year=now().year,
        created_at__month=now().month
    ).count()

    remaining = max(limit - monthly_count, 0)

    if monthly_count >= limit:
        messages.error(request, "Monthly mock interview quota reached.")
        return redirect("dashboard")

    if request.method == "POST":
        interview_type = request.POST.get("interview_type")
        target_role = request.POST.get("target_role")
        scheduled_at_raw = request.POST.get("scheduled_at")

        dt = parse_datetime(scheduled_at_raw)

        if dt and is_naive(dt):
            dt = make_aware(dt)

        MockInterview.objects.create(
            user=user,
            interview_type=interview_type,
            target_role=target_role,
            scheduled_at=dt,
            status="scheduled"
        )

        messages.success(request, "Mock interview scheduled.")
        return redirect("dashboard")

    return render(request, "consultant/schedule_mock_interview.html", {
        "remaining": remaining,
        "limit": limit
    })





#adminviewmockinterview
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_mock_interviews(request):
    interviews = MockInterview.objects.all().order_by("-created_at")

    if request.method == "POST":
        interview_id = request.POST.get("id")
        meeting_link = request.POST.get("meeting_link")
        feedback = request.POST.get("feedback")
        status = request.POST.get("status")

        interview = MockInterview.objects.get(id=interview_id)
        interview.meeting_link = meeting_link
        interview.feedback = feedback
        interview.status = status
        interview.save()

        return redirect("admin-mock-interviews")

    return render(request, "consultant/admin_mock_interviews.html", {
        "interviews": interviews
    })



@login_required
def my_mock_interviews(request):
    interviews = MockInterview.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "consultant/my_mock_interviews.html", {
        "interviews": interviews
    })
