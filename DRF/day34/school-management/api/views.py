# api/views.py

from rest_framework import viewsets
from .models import School, Teacher, Student, Subject
from .serializers import (
    SchoolSerializer,
    StudentNestedSerializer,
    StudentPKSerializer,
    StudentStringSerializer,
    StudentHyperlinkSerializer,
    TeacherNestedSerializer,
    TeacherPKSerializer,
    TeacherStringSerializer,
    TeacherHyperlinkSerializer,
    SubjectSerializer
)

class SchoolViewSet(viewsets.ModelViewSet):
    # includes nested students display
    queryset = School.objects.prefetch_related('students').all()
    serializer_class = SchoolSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('school').all()
    serializer_class = StudentNestedSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.prefetch_related('subjects').all()
    serializer_class = TeacherNestedSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.prefetch_related('teachers').all()
    serializer_class = SubjectSerializer

### Variant viewsets (read only) to show different serializers

class StudentVariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.select_related('school').all()

    def get_serializer_class(self):
        style = self.request.query_params.get('style')
        if style == 'pk':
            return StudentPKSerializer
        elif style == 'string':
            return StudentStringSerializer
        elif style == 'hyperlink':
            return StudentHyperlinkSerializer
        else:
            return StudentNestedSerializer

class TeacherVariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.prefetch_related('subjects').all()

    def get_serializer_class(self):
        style = self.request.query_params.get('style')
        if style == 'pk':
            return TeacherPKSerializer
        elif style == 'string':
            return TeacherStringSerializer
        elif style == 'hyperlink':
            return TeacherHyperlinkSerializer
        else:
            return TeacherNestedSerializer
