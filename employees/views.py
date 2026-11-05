from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, Count, Sum
from .models import User, Employee, Department, LeaveRequest, Attendance, Payroll, Announcement
from .forms import EmployeeForm, LeaveRequestForm, AttendanceForm, PayrollForm, DepartmentForm

# Role-based Mixins
class AdminHRRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['ADMIN', 'HR'] or self.request.user.is_superuser

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN' or self.request.user.is_superuser

# Dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'employees/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_employees'] = Employee.objects.count()
        context['active_employees'] = Employee.objects.filter(employment_status='Active').count()
        context['on_leave'] = Employee.objects.filter(employment_status='On Leave').count()
        context['total_departments'] = Department.objects.count()
        context['recent_employees'] = Employee.objects.select_related('department').order_by('-id')[:5]
        context['recent_announcements'] = Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
        return context

# Employee Views
class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        dept = self.request.GET.get('department')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search) | 
                Q(employee_id__icontains=search) |
                Q(email__icontains=search)
            )
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

    def form_valid(self, form):
        # Auto-create User account for the employee
        email = form.cleaned_data.get('email')
        base_username = email.split('@')[0] if email else 'emp_user'
        username = base_username
        idx = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{idx}"
            idx += 1
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password='Password@123',
            first_name=form.cleaned_data.get('first_name', ''),
            last_name=form.cleaned_data.get('last_name', ''),
            role='EMPLOYEE'
        )
        form.instance.user = user
        messages.success(self.request, f"Employee {user.first_name} {user.last_name} created successfully! (Login username: {username})")
        return super().form_valid(form)

class EmployeeUpdateView(LoginRequiredMixin, AdminHRRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        messages.success(self.request, f"Employee {form.instance.first_name} {form.instance.last_name} updated successfully.")
        return super().form_valid(form)

class EmployeeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Employee record deleted successfully.")
        return super().delete(request, *args, **kwargs)

# Department Views
class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'employees/department_list.html'
    context_object_name = 'departments'

class DepartmentCreateView(LoginRequiredMixin, AdminHRRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('department_list')

    def form_valid(self, form):
        messages.success(self.request, f"Department '{form.instance.name}' added successfully.")
        return super().form_valid(form)

# Leave Views
class LeaveListView(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'employees/leave_list.html'
    context_object_name = 'leave_requests'
    
    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'HR'] or self.request.user.is_superuser:
            return LeaveRequest.objects.all().order_by('-created_at')
        if hasattr(self.request.user, 'employee_profile'):
            return LeaveRequest.objects.filter(employee=self.request.user.employee_profile).order_by('-created_at')
        return LeaveRequest.objects.none()

class LeaveApplyView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'employees/leave_form.html'
    success_url = reverse_lazy('leave_list')

    def form_valid(self, form):
        if not hasattr(self.request.user, 'employee_profile'):
            messages.error(self.request, "Only registered employees can submit leave requests.")
            return redirect('leave_list')
        form.instance.employee = self.request.user.employee_profile
        messages.success(self.request, "Leave request submitted successfully.")
        return super().form_valid(form)

def approve_leave(request, pk):
    if request.user.role not in ['ADMIN', 'HR'] and not request.user.is_superuser:
        messages.error(request, "Permission denied.")
        return redirect('leave_list')
    leave = get_object_or_404(LeaveRequest, pk=pk)
    status = request.GET.get('status')
    if status in ['Approved', 'Rejected']:
        leave.status = status
        if hasattr(request.user, 'employee_profile'):
            leave.approved_by = request.user.employee_profile
        leave.save()
        if status == 'Approved':
            emp = leave.employee
            emp.employment_status = 'On Leave'
            emp.save()
        messages.success(request, f"Leave request marked as {status}.")
    return redirect('leave_list')

# Attendance Views
class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'employees/attendance_list.html'
    context_object_name = 'attendance_records'
    ordering = ['-date']

class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'employees/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

    def form_valid(self, form):
        messages.success(self.request, "Attendance record saved.")
        return super().form_valid(form)

# Payroll Views
class PayrollListView(LoginRequiredMixin, ListView):
    model = Payroll
    template_name = 'employees/payroll_list.html'
    context_object_name = 'payrolls'
    ordering = ['-year', '-month']

class PayrollCreateView(LoginRequiredMixin, AdminHRRequiredMixin, CreateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'employees/payroll_form.html'
    success_url = reverse_lazy('payroll_list')

    def form_valid(self, form):
        messages.success(self.request, "Payroll record generated successfully.")
        return super().form_valid(form)

# Announcements
class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'employees/announcement_list.html'
    context_object_name = 'announcements'
    ordering = ['-created_at']
