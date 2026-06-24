from django.shortcuts import render
from student.models import students
from .serializers import StudentsSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])  # this view will only accept GET and POST requests
def studentsView(request):
    if request.method == "GET":
        # GET = user wants to see data
        student = students.objects.all()  # get all students from database
        serializer = StudentsSerializer(student, many=True)  # convert data to JSON (many=True because it's a list)
        return Response(serializer.data, status=status.HTTP_200_OK)  # send JSON back with 200 OK

    elif request.method == "POST":
        # POST = user wants to add new data
        serializer = StudentsSerializer(data=request.data)  # load incoming data into serializer

        if serializer.is_valid():  # check if data is correct/complete
            serializer.save()  # save new student to database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # success response

        print(serializer.errors)  # show what went wrong (for debugging)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # send error response