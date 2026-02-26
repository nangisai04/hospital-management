from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from billing.models import Bill

User = get_user_model()


def home_view(request):
    """Display login choice page for patients vs doctors."""
    return render(request, "home.html")


def patient_register_view(request):
    """Patient registration page."""
    error_message = None
    success_message = None
    
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        phone = request.POST.get("phone", "").strip()
        date_of_birth = request.POST.get("date_of_birth")
        gender = request.POST.get("gender", "M")
        
        # Validation
        if not all([first_name, last_name, email, username, password, phone, date_of_birth]):
            error_message = "All fields are required."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."
        elif password != confirm_password:
            error_message = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different one."
        elif User.objects.filter(email=email).exists():
            error_message = "Email already registered. Please use a different email."
        else:
            try:
                # Create user account
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create patient profile
                patient = Patient.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    address="",
                    city=""
                )
                
                success_message = "Account created successfully! Please login."
                # Clear form
                return render(request, "patient_register.html", {
                    'success_message': success_message,
                })
            except IntegrityError:
                error_message = "Error creating account. Please try again."
    
    return render(request, "patient_register.html", {'error_message': error_message})


def doctor_register_view(request):
    """Doctor registration page."""
    error_message = None
    success_message = None
    
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        phone = request.POST.get("phone", "").strip()
        specialization = request.POST.get("specialization", "").strip()
        experience = request.POST.get("experience", "0")
        
        # Validation
        if not all([first_name, last_name, email, username, password, phone, specialization, experience]):
            error_message = "All fields are required."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."
        elif password != confirm_password:
            error_message = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different one."
        elif User.objects.filter(email=email).exists():
            error_message = "Email already registered. Please use a different email."
        else:
            try:
                # Create user account
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create doctor profile
                doctor = Doctor.objects.create(
                    user=user,
                    specialization=specialization,
                    experience=int(experience),
                    phone=phone
                )
                
                success_message = "Doctor account created successfully! Please login."
                # Clear form
                return render(request, "doctor_register.html", {
                    'success_message': success_message,
                })
            except IntegrityError:
                error_message = "Error creating account. Please try again."
    
    return render(request, "doctor_register.html", {'error_message': error_message})


def patient_login_view(request):
    """Patient/Customer login page."""
    error_message = None
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error_message = "Please enter both username and password."
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if user is a patient (not a doctor)
                if not Doctor.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('/patient-dashboard/')
                else:
                    error_message = "This account is registered as a doctor. Please use doctor login."
            else:
                error_message = "Invalid username or password. Please try again."

    return render(request, "patient_login.html", {'error_message': error_message})


def doctor_login_view(request):
    """Doctor login page."""
    error_message = None
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error_message = "Please enter both username and password."
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if user is a doctor
                if Doctor.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('/doctor-dashboard/')
                else:
                    error_message = "This account is not registered as a doctor. Please use patient login."
            else:
                error_message = "Invalid username or password. Please try again."

    return render(request, "doctor_login.html", {'error_message': error_message})


@login_required(login_url='patient_login')
def patient_dashboard_view(request):
    """Display patient dashboard with appointments and billing."""
    
    # Get current patient
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient = None
    
    context = {
        'user': request.user,
        'patient': patient,
        'total_doctors': Doctor.objects.count(),
        'my_appointments': Appointment.objects.filter(patient=patient).order_by('-appointment_date')[:10] if patient else [],
        'my_bills': Bill.objects.filter(patient=patient).order_by('-issue_date')[:10] if patient else [],
        'pending_bills': Bill.objects.filter(patient=patient, status='pending') if patient else [],
        'user_type': 'patient',
    }
    
    return render(request, "patient_dashboard.html", context)

# --- extra list views for admin links ------------------------------------------------
@login_required(login_url='admin_login')
def doctors_list_view(request):
    """Show full list of doctors on dedicated page (for admins)."""
    if not request.user.is_staff:
        return redirect('home')
    doctors = Doctor.objects.all()
    return render(request, 'doctors_list.html', {'doctors': doctors, 'user': request.user})


@login_required(login_url='admin_login')
def patients_list_view(request):
    """Show full list of patients on dedicated page (for admins)."""
    if not request.user.is_staff:
        return redirect('home')
    patients = Patient.objects.all()
    return render(request, 'patients_list.html', {'patients': patients, 'user': request.user})

@login_required(login_url='doctor_login')
def doctor_dashboard_view(request):
    """Display doctor dashboard with appointments and patient information."""
    
    # Get current doctor
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        doctor = None
    
    context = {
        'user': request.user,
        'doctor': doctor,
        'total_patients': Patient.objects.count(),
        'my_appointments': Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')[:10] if doctor else [],
        'scheduled_appointments': Appointment.objects.filter(doctor=doctor, status='scheduled').count() if doctor else 0,
        'completed_appointments': Appointment.objects.filter(doctor=doctor, status='completed').count() if doctor else 0,
        'user_type': 'doctor',
    }
    
    return render(request, "doctor_dashboard.html", context)


@login_required(login_url='login')
def dashboard_view(request):
    """Display hospital management dashboard with statistics and quick info."""
    
    # Calculate total billing
    total_billing = sum(bill.amount for bill in Bill.objects.all())
    pending_billing = sum(bill.amount for bill in Bill.objects.filter(status='pending'))
    
    context = {
        'total_doctors': Doctor.objects.count(),
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_billing': f"${total_billing:,.2f}",
        'pending_billing': f"${pending_billing:,.2f}",
        'scheduled_appointments': Appointment.objects.filter(status='scheduled').count(),
        'completed_appointments': Appointment.objects.filter(status='completed').count(),
        'pending_bills': Bill.objects.filter(status='pending').count(),
        'paid_bills': Bill.objects.filter(status='paid').count(),
        'doctors': Doctor.objects.all()[:5],
        'recent_patients': Patient.objects.all()[:5],
        'recent_appointments': Appointment.objects.all()[:5],
        'user': request.user,
        'is_doctor': Doctor.objects.filter(user=request.user).exists(),
    }
    
    return render(request, "dashboard.html", context)


@login_required(login_url='login')
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('home')


def admin_login_view(request):
    """Admin/Chairman login page."""
    error_message = None
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error_message = "Please enter both username and password."
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if user is staff/admin
                if user.is_staff:
                    login(request, user)
                    return redirect('/admin-dashboard/')
                else:
                    error_message = "This account does not have admin privileges. Please use appropriate login."
            else:
                error_message = "Invalid username or password. Please try again."

    return render(request, "admin_login.html", {'error_message': error_message})


@login_required(login_url='admin_login')
def admin_dashboard_view(request):
    """Display admin/chairman dashboard with hospital overview and free doctors."""
    
    # Check if user is admin
    if not request.user.is_staff:
        return redirect('home')
    
    # Get all doctors with their appointment counts
    all_doctors = Doctor.objects.all()
    
    # Calculate free doctors (those with less than 3 scheduled appointments today)
    from django.utils import timezone
    from datetime import timedelta
    
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    
    doctors_with_appointments = []
    free_doctors = []
    
    for doctor in all_doctors:
        scheduled_today = Appointment.objects.filter(
            doctor=doctor,
            status='scheduled',
            appointment_date__date=today
        ).count()
        
        doctors_with_appointments.append({
            'doctor': doctor,
            'scheduled_today': scheduled_today,
            'is_free': scheduled_today < 3
        })
        
        if scheduled_today < 3:
            free_doctors.append(doctor)
    
    # Get all appointments
    all_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-appointment_date')
    
    # Get statistics
    total_billing = sum(bill.amount for bill in Bill.objects.all())
    pending_billing = sum(bill.amount for bill in Bill.objects.filter(status='pending'))
    
    context = {
        'user': request.user,
        'total_doctors': all_doctors.count(),
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_billing': f"${total_billing:,.2f}",
        'pending_billing': f"${pending_billing:,.2f}",
        'scheduled_count': Appointment.objects.filter(status='scheduled').count(),
        'completed_count': Appointment.objects.filter(status='completed').count(),
        'cancelled_count': Appointment.objects.filter(status='cancelled').count(),
        'scheduled_appointments': Appointment.objects.filter(status='scheduled').count(),
        'completed_appointments': Appointment.objects.filter(status='completed').count(),
        'cancelled_appointments': Appointment.objects.filter(status='cancelled').count(),
        'free_doctors': free_doctors,
        'doctors_with_appointments': doctors_with_appointments,
        'all_appointments': all_appointments[:20],  # Latest 20 appointments
        'pending_bills': Bill.objects.filter(status='pending').count(),
        # list pages will fetch full sets separately
        'user_type': 'admin',
    }
    
    return render(request, "admin_dashboard.html", context)