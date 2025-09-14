from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import MiniProject
from .serializers import (
    MiniProjectSerializer,
    MiniProjectUpdateSerializer,
    RegisterSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

User = get_user_model()

# Permission utility
from rest_framework import permissions

class IsTrainerOrAssignedTrainee(permissions.BasePermission):
    """
    Trainer (is_staff=True): full access.
    Trainee: read own assigned projects; update limited fields of own projects.
    """

    def has_permission(self, request, view):
        # allow registration (handled by separate view) even if unauthenticated
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        if obj.assigned_to_id == user.id:
            if request.method in permissions.SAFE_METHODS:
                return True
            if request.method in ("PUT", "PATCH"):
                return True
        return False

class MiniProjectViewSet(viewsets.ModelViewSet):
    queryset = MiniProject.objects.select_related("assigned_to", "assigned_by").all().order_by("-created_at")
    serializer_class = MiniProjectSerializer
    permission_classes = [IsTrainerOrAssignedTrainee]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority", "assigned_to"]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_authenticated and user.is_staff:
            return qs
        if user.is_authenticated:
            return qs.filter(assigned_to_id=user.id)
        return qs.none()

    def get_serializer_class(self):
        if self.action in ("partial_update", "update"):
            return MiniProjectUpdateSerializer
        return MiniProjectSerializer
    
    

    def perform_create(self, serializer):
        # assigned_by set in MiniProjectSerializer.create() using request.user
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail":"Only trainers can delete projects."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    # on successful create, signals will send welcome email


from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([AllowAny])
def public_mini_projects(request):
    """
    Return all mini projects publicly (for HomePage)
    """
    projects = MiniProject.objects.select_related("assigned_to", "assigned_by").all().order_by("-created_at")
    serializer = MiniProjectSerializer(projects, many=True)
    return Response(serializer.data)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import UserSerializer

User = get_user_model()

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def trainees_list(request):
    """
    Return all users with role 'trainee' (is_staff=False)
    """
    trainees = User.objects.filter(is_staff=False)
    serializer = UserSerializer(trainees, many=True)
    return Response(serializer.data)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MiniProject
from .serializers import MiniProjectSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mini_project_report(request):
    user = request.user
    if not user.is_staff:
        return Response({"detail": "Only trainers can view reports."}, status=403)
    
    # Get all mini projects assigned by this trainer
    projects = MiniProject.objects.filter(assigned_by=user).select_related("assigned_to").order_by("-created_at")
    
    # Prepare report data
    report = [
        {
            "id": p.id,
            "title": p.title,
            "assigned_to": p.assigned_to.username if p.assigned_to else None,
            "status": p.status,
            "progress": p.progress,
            "due_date": p.due_date,
            "completed": p.status == "completed"
        }
        for p in projects
    ]
    
    return Response(report)
