from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count, Sum
from .models import Employee, Department, LeaveRequest, Attendance, Payroll, Announcement
from .forms import EmployeeForm, LeaveRequestForm, AttendanceForm, PayrollForm, DepartmentForm

# Role-based Mixins
class AdminHRRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['ADMIN', 'HR']

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

# Dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'employees/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_employees'] = Employee.objects.count()
        context['active_employees'] = Employee.objects.filter(employment_status='Active').count()
        context['on_leave'] = Employee.objects.filter(employment_status='On Leave').count()
        context['total_departments'] = Department.objects.count()
        context['recent_announcements'] = Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
        return context

# Employee Views
class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        dept = self.request.GET.get('department')
        if search:
            queryset = queryset.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(employee_id__icontains=search))
        if dept:
            queryset = queryset.filter(department_id=dept)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

class EmployeeCreateView(LoginRequiredMixin, AdminHRRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeUpdateView(LoginRequiredMixin, AdminHRRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

# Department Views
class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'employees/department_list.html'

class DepartmentCreateView(LoginRequiredMixin, AdminHRRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('department_list')

# Leave Views
class LeaveListView(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'employees/leave_list.html'
    
    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'HR']:
            return LeaveRequest.objects.all().order_by('-created_at')
        return LeaveRequest.objects.filter(employee=self.request.user.employee_profile).order_by('-created_at')

class LeaveApplyView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'employees/leave_form.html'
    success_url = reverse_lazy('leave_list')

    def form_valid(self, form):
        form.instance.employee = self.request.user.employee_profile
        return super().form_valid(form)

def approve_leave(request, pk):
    if request.user.role not in ['ADMIN', 'HR']:
        return redirect('leave_list')
    leave = get_object_or_404(LeaveRequest, pk=pk)
    status = request.GET.get('status')
    if status in ['Approved', 'Rejected']:
        leave.status = status
        leave.approved_by = request.user.employee_profile
        leave.save()
        # Update employee status if approved
        if status == 'Approved':
            emp = leave.employee
            emp.employment_status = 'On Leave'
            emp.save()
    return redirect('leave_list')

# Attendance Views
class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'employees/attendance_list.html'

class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'employees/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

# Payroll Views
class PayrollListView(LoginRequiredMixin, ListView):
    model = Payroll
    template_name = 'employees/payroll_list.html'

class PayrollCreateView(LoginRequiredMixin, AdminHRRequiredMixin, CreateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'employees/payroll_form.html'
    success_url = reverse_lazy('payroll_list')

# Announcements
class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'employees/announcement_list.html'
