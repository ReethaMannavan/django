from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import LeaveRequest

# List view for all leave requests
class LeaveListView(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'leave/leave_list.html'
    context_object_name = 'leaves'
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.filter(employee=user)


# Create a new leave request
class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    fields = ['reason']
    template_name = 'leave/leave_form.html'
    success_url = reverse_lazy('leave-list')

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)


# Update leave request
class LeaveUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LeaveRequest
    fields = ['reason']
    template_name = 'leave/leave_form.html'
    success_url = reverse_lazy('leave-list')

    def test_func(self):
        leave = self.get_object()
        return self.request.user == leave.employee or self.request.user.is_superuser


# Delete leave request
class LeaveDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LeaveRequest
    template_name = 'leave/leave_confirm_delete.html'
    success_url = reverse_lazy('leave-list')

    def test_func(self):
        leave = self.get_object()
        return self.request.user == leave.employee or self.request.user.is_superuser


# Approve leave (staff/superuser only)
def approve_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.user.is_staff or request.user.is_superuser:
        leave.status = 'APPROVED'
        leave.save()
        messages.success(request, "Leave approved successfully!")
    else:
        messages.error(request, "You are not authorized to approve leaves.")
    return redirect('leave-list')


# Reject leave (staff/superuser only)
def reject_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.user.is_staff or request.user.is_superuser:
        leave.status = 'REJECTED'
        leave.save()
        messages.success(request, "Leave rejected successfully!")
    else:
        messages.error(request, "You are not authorized to reject leaves.")
    return redirect('leave-list')
