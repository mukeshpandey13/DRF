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

@api_view(['GET', 'PUT', 'DELETE'])  # this view accepts GET, PUT, and DELETE requests
def studentDetailView(request, pk):  # pk = primary key (id of the student we want)
    try:
        student = students.objects.get(pk=pk)  # try to find a single student with this id

    except students.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  # if no such student exists, send 404 (not found)

    if request.method == 'GET':
        serializer = StudentsSerializer(student)  # convert single student object to JSON
        return Response(serializer.data, status=status.HTTP_200_OK)  # send student's data back

    elif request.method == "PUT":
        # PUT = update existing student's data
        serializer = StudentsSerializer(student, data=request.data)  # load new data INTO the existing student object
        if serializer.is_valid():  # check if new data is correct/complete
            serializer.save()  # update the student in database
            return Response(serializer.data, status=status.HTTP_200_OK)  # send updated data back
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # send error response

    elif request.method == 'DELETE':
        # DELETE = remove the student
        student.delete()  # delete this student from database
        return Response(status=status.HTTP_204_NO_CONTENT)  # success, but no data to send back


# class base view
from rest_framework.views import APIView  # base class for class-based API views
from employees.models import Employee  # the Employee model (database table)
from .serializers import EmployeeSerializer  # converts Employee data to/from JSON

class Employees(APIView):  # class-based view (alternative to @api_view function-based views)
    def get(self, request):  # handles GET requests (no need for if/elif method checks!)
        employees = Employee.objects.all()  # get all employees from database
        serializer = EmployeeSerializer(employees, many=True)  # convert list of employees to JSON
        return Response(serializer.data, status=status.HTTP_200_OK)  # send JSON back with 200 OK

    def post(self, request):  # handles POST requests (called automatically when a POST hits this URL)
        serializer = EmployeeSerializer(data=request.data)  # load incoming data into serializer
        if serializer.is_valid():  # check if data is correct/complete
            serializer.save()  # save new employee to database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # success response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # send error response


from django.http import Http404

class EmployeeDetails(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk = pk)
        except Employee.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
