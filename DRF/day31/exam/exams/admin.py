from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

class AdminTestView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        return Response({"message": "Admin access granted!"})


from django.contrib import admin
from .models import Exam, Question, StudentExam

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(StudentExam)
