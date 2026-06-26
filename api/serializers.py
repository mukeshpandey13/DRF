from rest_framework import serializers
from student.models import students

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = students
        fields = "__all__"

# for class base
from employees.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
