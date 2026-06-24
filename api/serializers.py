from rest_framework import serializers
from student.models import students

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = students
        fields = "__all__"