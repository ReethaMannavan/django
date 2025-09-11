from rest_framework import serializers
from django.contrib.auth.models import User

# Student registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Student profile serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']




from .models import Exam, Question, StudentExam

# Question Serializer
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option']

# Exam Serializer (nested questions)
class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'questions', 'created_at', 'updated_at']

# Serializer for creating Exam (admin) without nested questions
class ExamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description']

# StudentExam Serializer
class StudentExamSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentExam
        fields = ['id', 'student', 'exam', 'score', 'completed_at']
