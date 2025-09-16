# api/serializers.py

from rest_framework import serializers
from .models import School, Teacher, Student, Subject

### Basic / Nested Serializers

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class TeacherNestedSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'subjects']

class StudentNestedSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField(read_only=True)  # or nested school if needed

    class Meta:
        model = Student
        fields = ['id', 'name', 'school']


class SchoolSerializer(serializers.ModelSerializer):
    students = StudentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = School
        fields = ['id', 'name', 'students']

### Variants for ForeignKey (Student.school)

class StudentPKSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        model = Student
        fields = ['id', 'name', 'school']

class StudentStringSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'school']

class StudentHyperlinkSerializer(serializers.HyperlinkedModelSerializer):
    school = serializers.HyperlinkedRelatedField(view_name='school-detail', queryset=School.objects.all())

    class Meta:
        model = Student
        fields = ['url', 'id', 'name', 'school']

### Variants for ManyToMany (Teacher.subjects)

class TeacherPKSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(many=True, queryset=Subject.objects.all())

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'subjects']

class TeacherStringSerializer(serializers.ModelSerializer):
    subjects = serializers.StringRelatedField(many=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'subjects']

class TeacherHyperlinkSerializer(serializers.HyperlinkedModelSerializer):
    subjects = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='subject-detail',
        queryset=Subject.objects.all()
    )

    class Meta:
        model = Teacher
        fields = ['url', 'id', 'name', 'subjects']
