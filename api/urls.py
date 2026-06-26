from django.urls import path
from .import views

urlpatterns = [
    path('students/', views.studentsView),
        path('student/<int:pk>/', views.studentDetailView),

        # .as_view used for class base view
        path('employees/', views.Employees.as_view()),
        path('employees/<int:pk>/',views.EmployeeDetails.as_view()),
]
