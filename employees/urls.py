from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Employees
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/add/', views.EmployeeCreateView.as_view(), name='employee_add'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    
    # Departments
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/add/', views.DepartmentCreateView.as_view(), name='department_add'),
    
    # Leave
    path('leave/', views.LeaveListView.as_view(), name='leave_list'),
    path('leave/apply/', views.LeaveApplyView.as_view(), name='leave_apply'),
    path('leave/<int:pk>/approve/', views.approve_leave, name='leave_approve'),
    
    # Attendance
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/mark/', views.AttendanceCreateView.as_view(), name='attendance_mark'),
    
    # Payroll
    path('payroll/', views.PayrollListView.as_view(), name='payroll_list'),
    path('payroll/generate/', views.PayrollCreateView.as_view(), name='payroll_generate'),
    
    # Announcements
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement_list'),
]
