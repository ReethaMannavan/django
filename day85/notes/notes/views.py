from django.shortcuts import render

# Create your views here.
# notes/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Note

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Note.objects.all()
        return Note.objects.filter(owner=user)

class NoteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'

    def test_func(self):
        note = self.get_object()
        return self.request.user.is_superuser or note.owner == self.request.user

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'notes/note_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'notes/note_form.html'

    def test_func(self):
        note = self.get_object()
        return self.request.user.is_superuser or note.owner == self.request.user

class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        note = self.get_object()
        return self.request.user.is_superuser or note.owner == self.request.user
