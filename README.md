# Hospital Management System

A Django-based hospital management application with user authentication, patient management, doctor profiles, appointment scheduling, and billing system.

## Features

✅ **User Authentication**
- Secure login system with error handling
- Professional login page with styling

✅ **Dashboard**
- View hospital statistics (doctors, patients, appointments, billing)
- Recent doctors list
- Recent patients list
- Recent appointments with status tracking
- Real-time billing information

✅ **Sample Data**
- 15 registered doctors with specializations
- 50 registered patients
- 60 appointments scheduled
- 99 billing records

✅ **Models**
- Patient: Store patient information (name, email, phone, address, medical history, allergies)
- Doctor: Manage doctor profiles (specialization, experience, contact)
- Appointment: Schedule and track appointments (date, status, notes)
- Bill: Track billing and payments (amount, status, dates)

## Installation & Setup

### 1. Install Dependencies
```bash
pip install django djangorestframework faker
```

### 2. Create Database Tables
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Populate Sample Data
```bash
python manage.py populate_data
```

This creates:
- 15 doctors with various specializations
- 50 patients with complete information
- 60 appointments
- 99 billing records

### 4. Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000/`

## Test Credentials

### Doctor Login
- **URL**: http://127.0.0.1:8000/doctor-login/
- **Username**: doctor1 (or doctor2, doctor3... doctor15)
- **Password**: password123

### Patient/Customer Login
- **URL**: http://127.0.0.1:8000/patient-login/
- **Username**: Create test patient or use existing patient credentials
- **Password**: password123

**Note**: To get patient login credentials, you'll need to register a patient account first or contact the admin to create one.

## Application Flow

1. **Home Page** (`/`) - Choose login type (Patient or Doctor)
2. **Patient Login** (`/patient-login/`) - Patient/Customer authentication
   - Redirects to Patient Dashboard
3. **Doctor Login** (`/doctor-login/`) - Doctor authentication
   - Redirects to Doctor Dashboard
4. **Logout** (`/logout/`) - Return to home page

## Patient Features

✅ **Patient Dashboard** (`/patient-dashboard/`)
- View personal information
- See all booked appointments
- Track appointment status
- Manage billing information
- View pending bills

## Doctor Features

✅ **Doctor Dashboard** (`/doctor-dashboard/`)
- View doctor profile and specialization
- See appointment schedule
- Track scheduled and completed appointments
- View patient information
- Monitor appointment statistics

## Directory Structure

```
hospital_management/
├── accounts/           # Authentication & user management
│   ├── views.py        # Login, dashboard, logout views
│   ├── models.py       # User model (uses Django default)
│   └── management/
│       └── commands/
│           └── populate_data.py  # Sample data generation
├── patients/           # Patient management
│   └── models.py       # Patient model
├── doctors/            # Doctor management
│   └── models.py       # Doctor model with specialization
├── appointments/       # Appointment scheduling
│   └── models.py       # Appointment model
├── billing/            # Billing system
│   └── models.py       # Bill model
├── hospital/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── templets/           # HTML templates
    ├── login.html      # Login page
    └── dashboard.html  # Dashboard page
```

## Template Features

### Login Page
- Professional gradient design
- Error message display
- Form validation
- Responsive layout

### Dashboard
- Statistics cards with counts
- Doctor listing table
- Patient listing table
- Appointment tracking with status
- Real-time billing information
- User profile information
- Logout button

## Future Enhancements

- Patient appointment booking
- Doctor availability scheduling
- Payment processing
- Medical records management
- Email notifications
- SMS alerts
- Mobile application
- API endpoints for external integrations

## Database Models

### Patient
- First/Last Name, Email, Phone
- Date of Birth, Gender
- Address, City
- Medical History, Allergies

### Doctor
- User Account
- Specialization
- Years of Experience
- Phone Number

### Appointment
- Patient & Doctor Association
- Appointment Date & Time
- Status (Scheduled, Completed, Cancelled)
- Reason & Notes

### Bill
- Patient & Appointment Association
- Amount & Description
- Status (Pending, Paid, Overdue)
- Issue, Due & Paid Dates

## Technologies Used

- **Framework**: Django 6.0.2
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS (responsive design)
- **Libraries**: Django REST Framework, Faker (sample data)
- **Python**: 3.13

## Support

For issues or questions, please check the Django documentation:
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
