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

## Deploying to Railway 🚀

This project is configured to run on Railway with minimal changes. Follow these steps:

1. **Prepare your repository**
   - Commit all changes, including `settings.py` updates (WhiteNoise middleware, static storage).
   - Ensure `Procfile` contains:
     ```
     web: gunicorn hospital.wsgi
     release: python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - Use the **root** `requirements.txt` (now a trimmed production file) for deployment. The original, full dependency list remains in `hospital_management/requirements.txt` for local development.
   - Create a `runtime.txt` at the **repository root** with a supported Python version (`python-3.11.13`). Render and other platforms read the root file.
   - **Render build command** must be a single line; do **not** include a trailing backslash or newline escape. Example:
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
     (The backslash inserted in the earlier log caused pip to receive an empty requirement and fail.)

2. **Create a Railway project**
   - Sign in to https://railway.app/ and click **New Project** → **Deploy from GitHub**.
   - Connect your GitHub account and select the repository containing this code.
   - Railway will detect Python and the `Procfile` automatically.

3. **Configure environment variables**
   - In the Railway project settings add:
     - `SECRET_KEY` – a strong secret for Django.
     - `DEBUG` – set to `False` for production.
     - `ALLOWED_HOSTS` – e.g. `*` or your Railway domain (e.g. `your-app.up.railway.app`).
     - `DATABASE_URL` – Railway will usually set this automatically when you add a PostgreSQL plugin.

4. **Add a database**
   - From the Railway dashboard add a plugin (PostgreSQL recommended).
   - The `DATABASE_URL` environment variable will be injected automatically.
   - Django's `dj_database_url` configuration handles the connection.

5. **Trigger deployment**
   - Deploy the project. Railway will run the buildpack, install dependencies, and execute the `release` command which runs migrations and collects static files.
   - Once build finishes, Railway will start the web process using Gunicorn via your `Procfile`.

6. **Verify the live app**
   - Open the Railway-generated URL (e.g. `https://<project>.up.railway.app`) in a browser.
   - You should see the application running with static assets served and the database migrated.

> 🔧 You can run `python manage.py collectstatic` locally before pushing if you want to preview static behavior.

By following these steps you'll have a live Django application on Railway with automatic migrations and static file handling. Feel free to adjust settings or add plugins (e.g. Redis, mail) as needed.

## Support

For issues or questions, please check the Django documentation:
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
