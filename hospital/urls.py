from django.contrib import admin
from django.urls import path
from accounts.views import (
    home_view, 
    patient_login_view,
    patient_register_view,
    doctor_login_view,
    doctor_register_view,
    admin_login_view,
    patient_dashboard_view,
    doctor_dashboard_view,
    admin_dashboard_view,
    dashboard_view, 
    logout_view,
    doctors_list_view,
    patients_list_view,
)

urlpatterns = [
    # custom admin list pages must appear before default admin route
    path('admin/doctors/', doctors_list_view, name='admin_doctors_list'),
    path('admin/patients/', patients_list_view, name='admin_patients_list'),
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('patient-login/', patient_login_view, name='patient_login'),
    path('patient-register/', patient_register_view, name='patient_register'),
    path('doctor-login/', doctor_login_view, name='doctor_login'),
    path('doctor-register/', doctor_register_view, name='doctor_register'),
    path('admin-login/', admin_login_view, name='admin_login'),
    path('patient-dashboard/', patient_dashboard_view, name='patient_dashboard'),
    path('doctor-dashboard/', doctor_dashboard_view, name='doctor_dashboard'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
]