from django.shortcuts import render
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from .models import Job, Application
from .forms import SignUpForm, StyledAuthenticationForm, JobForm, JobSearchForm, ApplicationForm

# Signup
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,"Signup successful!")
            return redirect(user.get_dashboard_url())
    else:
        form = SignUpForm()
    return render(request,'registration/signup.html',{'form':form})

# Logout via POST
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('jobapp:job_list')

# Mixins
class EmployerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'employer'
    def handle_no_permission(self):
        messages.error(self.request,"Employer access required")
        return redirect('login')

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

# Job views
class JobCreateView(LoginRequiredMixin, EmployerRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request,"Job posted successfully")
        return super().form_valid(form)

class JobListView(ListView):
    model = Job
    paginate_by = 8
    template_name = 'jobs/job_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = JobSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        loc = self.request.GET.get('location')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(company__icontains=q) | Q(description__icontains=q))
        if loc:
            qs = qs.filter(location__icontains=loc)
        return qs

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application_form'] = ApplicationForm()
        context['has_applied'] = False
        if self.request.user.is_authenticated and self.request.user.role == 'applicant':
            context['has_applied'] = Application.objects.filter(job=self.object, applicant=self.request.user).exists()
        return context

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(Job, pk=kwargs['job_pk'])
        if request.user.role != 'applicant':
            messages.error(request,"Only applicants can apply")
            return redirect(self.job.get_absolute_url())
        if Application.objects.filter(job=self.job, applicant=request.user).exists():
            messages.error(request,"You already applied")
            return redirect(self.job.get_absolute_url())
        return super().dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        form.instance.job = self.job
        form.instance.applicant = self.request.user
        response = super().form_valid(form)
        # email
        try:
            from django.core.mail import send_mail
            send_mail(
                subject=f"Application received for {self.job.title}",
                message="Thank you for applying.",
                from_email=None,
                recipient_list=[self.request.user.email],
                fail_silently=False,
            )
        except Exception:
            messages.warning(self.request,"Application saved but email failed")
        messages.success(self.request,"Application submitted")
        return response

    def get_success_url(self):
        return self.job.get_absolute_url()

class EmployerDashboardView(LoginRequiredMixin, EmployerRequiredMixin, TemplateView):
    template_name = 'jobs/employer_dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.filter(created_by=self.request.user)
        return context

class JobUpdateView(LoginRequiredMixin, EmployerRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm

class JobDeleteView(LoginRequiredMixin, EmployerRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('jobapp:employer_dashboard')

