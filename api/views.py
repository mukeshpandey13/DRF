from django.shortcuts import render, get_object_or_404
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
# from rest_framework.views import APIView  # base class for class-based API views
# from employees.models import Employee  # the Employee model (database table)
# from .serializers import EmployeeSerializer  # converts Employee data to/from JSON

# class Employees(APIView):  # class-based view (alternative to @api_view function-based views)
#     def get(self, request):  # handles GET requests (no need for if/elif method checks!)
#         employees = Employee.objects.all()  # get all employees from database
#         serializer = EmployeeSerializer(employees, many=True)  # convert list of employees to JSON
#         return Response(serializer.data, status=status.HTTP_200_OK)  # send JSON back with 200 OK

#     def post(self, request):  # handles POST requests (called automatically when a POST hits this URL)
#         serializer = EmployeeSerializer(data=request.data)  # load incoming data into serializer
#         if serializer.is_valid():  # check if data is correct/complete
#             serializer.save()  # save new employee to database
#             return Response(serializer.data, status=status.HTTP_201_CREATED)  # success response
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # send error response

# from django.http import Http404  # built-in exception that returns a 404 page/response

# class EmployeeDetails(APIView):

#     def get_object(self, pk):  # helper method - reused by get/put/delete below
#         try:
#             return Employee.objects.get(pk=pk)  # try to find employee with this id
#         except Employee.DoesNotExist:
#             raise Http404  # if not found, raise 404 (DRF automatically converts this to a proper 404 response)

#     def get(self, request, pk):  # handles GET request - view single employee
#         employee = self.get_object(pk)  # reuse helper to fetch employee
#         serializer = EmployeeSerializer(employee)  # convert to JSON
#         return Response(serializer.data, status=status.HTTP_200_OK)  # send data back

#     def put(self, request, pk):  # handles PUT request - update employee
#         employee = self.get_object(pk)  # reuse helper to fetch employee
#         serializer = EmployeeSerializer(employee, data=request.data)  # load new data into existing employee
#         if serializer.is_valid():  # check if new data is valid
#             serializer.save()  # update employee in database
#             return Response(serializer.data, status=status.HTTP_200_OK)  # send updated data back
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # send error response

#     def delete(self, request, pk):  # handles DELETE request - remove employee
#         employee = self.get_object(pk)  # reuse helper to fetch employee
#         employee.delete()  # delete from database
#         return Response(status=status.HTTP_204_NO_CONTENT)  # success, nothing to send back



######### we comment clas base view to use mixins #####################
"""
from rest_framework import mixins, generics  # mixins = reusable chunks of common behavior (list, create, etc.)
from employees.models import Employee
from .serializers import EmployeeSerializer

class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()  # tells DRF which records this view works with
    serializer_class = EmployeeSerializer  # tells DRF which serializer to use

    # getting all the object
    def get(self, request):
        return self.list(request)  # ListModelMixin gives us this - returns all employees as JSON

    # create the object
    def post(self, request):
        return self.create(request)  # CreateModelMixin gives us this - validates + saves new employee


class EmployeeDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)  # RetrieveModelMixin gives us this - gets ONE employee by pk

    def put(self, request, pk):
        return self.update(request, pk)  # UpdateModelMixin gives us this - validates + updates employee

    def delete(self, request, pk):
        return self.destroy(request, pk)  # DestroyModelMixin gives us this - deletes employee
"""


"""
###################### Generic ########################
from rest_framework import mixins, generics
from employees.models import Employee
from .serializers import EmployeeSerializer

# class Employees(generics.ListAPIView, generics.CreateAPIView):  # alternative way - combining two generics manually
class Employees(generics.ListCreateAPIView):  # built-in combo of List + Create, already merged for you
    queryset = Employee.objects.all()  # data this view works with
    serializer_class = EmployeeSerializer  # how to convert data to/from JSON
    # no get()/post() needed - ListCreateAPIView already has them built in!

# class EmployeeDetails(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):  # alternative manual combo
class EmployeeDetails(generics.RetrieveUpdateDestroyAPIView):  # built-in combo of Retrieve + Update + Destroy
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'  # tells DRF which field to use when looking up a single object (default is already 'pk', so this line is optional here)
    # no get()/put()/delete() needed - all built in!

"""

"""
######################## Generic ##################
from rest_framework import mixins, generics, viewsets
from employees.models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewset(viewsets.ViewSet):  # ViewSet = combines ALL CRUD actions into ONE class

    def list(self, request):  # handles GET /employees/ -> returns all employees
        queryset = Employee.objects.all()  # get all employees from database
        serializer = EmployeeSerializer(queryset, many=True)  # convert list to JSON
        return Response(serializer.data)  # send JSON back

    def create(self, request):  # handles POST /employees/ -> creates a new employee
        serializer = EmployeeSerializer(data=request.data)  # load incoming data into serializer
        if serializer.is_valid():  # check if data is correct/complete
            serializer.save()  # save new employee to database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # success response
        return Response(serializer.errors)  # send back validation errors

    def retrieve(self, request, pk=None):  # handles GET /employees/<pk>/ -> returns one employee
        employee = get_object_or_404(Employee, pk=pk)  # find employee by pk, auto-404 if not found
        serializer = EmployeeSerializer(employee)  # convert single employee to JSON
        return Response(serializer.data, status=status.HTTP_200_OK)  # send data back

    def update(self, request, pk):  # handles PUT /employees/<pk>/ -> updates one employee
        employee = get_object_or_404(Employee, pk=pk)  # find employee by pk, auto-404 if not found
        serializer = EmployeeSerializer(employee, data=request.data)  # load new data into existing employee
        if serializer.is_valid():  # check if new data is valid
            serializer.save()  # update employee in database
            return Response(serializer.data, status=status.HTTP_200_OK)  # send updated data back
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # send error response

    def destroy(self, request, pk=None):  # handles DELETE /employees/<pk>/ -> deletes one employee
        employee = get_object_or_404(Employee, pk=pk)  # find employee by pk, auto-404 if not found
        employee.delete()  # delete from database
        return Response(
            {"message": "Employee deleted successfully."},  # custom confirmation message
            status=status.HTTP_204_NO_CONTENT
        )
"""

from rest_framework import mixins, generics, viewsets
from employees.models import Employee
from .serializers import EmployeeSerializer
from .paginations import CustomPagination
from employees.filters import EmployeeFilter

class EmployeeViewset(viewsets.ModelViewSet):  # gives you ALL 5 actions (list, create, retrieve, update, destroy) for free

    queryset = Employee.objects.all()  # data this viewset works with
    serializer_class = EmployeeSerializer  # how to convert data to/from JSON
    # no list()/create()/retrieve()/update()/destroy() needed - all built in!

    # Pagination 
    pagination_class = CustomPagination

    # Filtering 
    # filterset_fields = ['designation']

    # customing filtering
    filterset_class = EmployeeFilter




#################### Blog and comments #########################

from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer
from rest_framework.filters import SearchFilter

class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    # search filter
    filter_backends = [SearchFilter]
    search_fields = ['blog_title','blog_body']

class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'