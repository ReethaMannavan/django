from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ConsultantRequest

@login_required
def request_consultant(request):
    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        message = request.POST.get('message')

        ConsultantRequest.objects.create(
            user=request.user,
            purpose=purpose,
            message=message
        )
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
