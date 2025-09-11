from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer

# Student registration API
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

# Student profile API (JWT protected)
class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

# Admin-only test API
class AdminTestView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        return Response({"message": "Admin access granted!"})




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_api_key.permissions import HasAPIKey
from .models import Exam, Question
from .serializers import ExamSerializer, ExamCreateSerializer, QuestionSerializer

# Admin: Create Exam
class AdminCreateExamView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        serializer = ExamCreateSerializer(data=request.data)
        if serializer.is_valid():
            exam = serializer.save()
            return Response(ExamSerializer(exam).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin: Add Question to Exam
class AdminAddQuestionView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(exam=exam)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#student

from rest_framework.permissions import IsAuthenticated
from .models import StudentExam
from .serializers import StudentExamSerializer, ExamSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# Student: List Exams
class ExamListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)

# Student: Submit Exam Result
from django.utils import timezone

class SubmitExamView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

        score = request.data.get("score", 0)  # For simplicity, sending score directly
        student_exam, created = StudentExam.objects.update_or_create(
            student=request.user,
            exam=exam,
            defaults={"score": score, "completed_at": timezone.now()}
        )
        serializer = StudentExamSerializer(student_exam)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    """
    API Landing Page for Online Exam Portal
    """
    def get(self, request):
        return Response({
            "message": "Welcome to Online Exam Portal API",
            "student_endpoints": {
                "register": "/register/ [POST]",
                "login": "/login/ [POST]",
                "token_refresh": "/token/refresh/ [POST]",
                "profile": "/profile/ [GET]",
                "list_exams": "/exams/ [GET]",
                "submit_exam": "/submit-exam/<exam_id>/ [POST]"
            },
            "admin_endpoints": {
                "admin_test": "/admin-test/ [GET]",
                "create_exam": "/admin-create-exam/ [POST]",
                "add_question": "/admin-add-question/<exam_id>/ [POST]"
            },
            "notes": [
                "Use JWT access token for student endpoints",
                "Use API Key for admin endpoints",
                "All data is JSON-based"
            ]
        })

