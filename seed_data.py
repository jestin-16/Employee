import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from employees.models import User, Department, Employee, Announcement
from datetime import date

def seed():
    print("--- Seeding Employee Management System Data ---")

    # 1. Admin Account
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin.role = 'ADMIN'
        admin.first_name = 'System'
        admin.last_name = 'Admin'
        admin.save()
        print("Created Admin user: admin / admin123")
    else:
        admin = User.objects.get(username='admin')

    # 2. HR Manager Account
    if not User.objects.filter(username='hrmanager').exists():
        hr_user = User.objects.create_user('hrmanager', 'hr@example.com', 'Password@123')
        hr_user.role = 'HR'
        hr_user.first_name = 'Sarah'
        hr_user.last_name = 'Jenkins'
        hr_user.save()
        print("Created HR Manager: hrmanager / Password@123")
    else:
        hr_user = User.objects.get(username='hrmanager')

    # 3. Departments
    dept_names = [
        ('Engineering & DevOps', 'Software Development and Cloud Operations'),
        ('Human Resources', 'Recruitment, Culture, and Employee Experience'),
        ('Product & Design', 'Product Management and UI/UX Design'),
        ('Finance & Payroll', 'Financial Planning and Salary Management'),
    ]
    depts = {}
    for name, desc in dept_names:
        dept, _ = Department.objects.get_or_create(name=name, defaults={'description': desc})
        depts[name] = dept
    print(f"Verified {len(depts)} departments.")

    # 4. Sample Employees
    emp_samples = [
        {
            'user': admin,
            'first_name': 'Alex',
            'last_name': 'Morgan',
            'email': 'alex.m@company.com',
            'phone': '+1-555-0101',
            'gender': 'Male',
            'date_of_birth': date(1990, 5, 12),
            'department': depts['Engineering & DevOps'],
            'designation': 'Lead Cloud Engineer',
            'employment_type': 'Full-Time',
            'employment_status': 'Active',
            'date_joined': date(2022, 1, 10),
            'salary': 115000.00,
            'address': '100 Silicon Blvd',
            'emergency_contact_name': 'Taylor Morgan',
            'emergency_contact_phone': '+1-555-0102'
        },
        {
            'user': hr_user,
            'first_name': 'Sarah',
            'last_name': 'Jenkins',
            'email': 'sarah.j@company.com',
            'phone': '+1-555-0201',
            'gender': 'Female',
            'date_of_birth': date(1993, 8, 20),
            'department': depts['Human Resources'],
            'designation': 'HR Manager',
            'employment_type': 'Full-Time',
            'employment_status': 'Active',
            'date_joined': date(2023, 3, 1),
            'salary': 85000.00,
            'address': '250 Maple Street',
            'emergency_contact_name': 'Michael Jenkins',
            'emergency_contact_phone': '+1-555-0202'
        }
    ]

    for d in emp_samples:
        Employee.objects.get_or_create(user=d['user'], defaults=d)

    # 5. Announcements
    if not Announcement.objects.exists():
        emp = Employee.objects.first()
        if emp:
            Announcement.objects.create(
                title='Quarterly Company All-Hands Meeting',
                content='Please join us this Thursday at 3:00 PM for our quarterly review and team recognition announcements.',
                posted_by=emp
            )
            Announcement.objects.create(
                title='Annual Benefits Open Enrollment',
                content='Health, wellness, and retirement contribution enrollment is open through the end of the month via the portal.',
                posted_by=emp
            )

    print("--- Database Seeding Complete ---")

if __name__ == '__main__':
    seed()
