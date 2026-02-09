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




from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from .models import ConsultantRequest

@staff_member_required
def admin_consultant_requests(request):
    requests = ConsultantRequest.objects.all().order_by('-created_at')

    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        ConsultantRequest.objects.filter(id=req_id).update(status=new_status)
        return redirect('admin-consultant-requests')

    return render(request, 'consultant/admin_requests.html', {
        'requests': requests
    })
