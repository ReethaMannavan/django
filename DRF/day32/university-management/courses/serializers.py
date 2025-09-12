from rest_framework import serializers
from .models import University, Department, Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'credits', 'department'] 



class DepartmentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(source='course_set', many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'university', 'courses'] 



class UniversitySerializer(serializers.ModelSerializer):
    # use source='department_set' because no related_name
    departments = DepartmentSerializer(source='department_set', many=True, read_only=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'location', 'departments']
