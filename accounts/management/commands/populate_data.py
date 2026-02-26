from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random
from faker import Faker

from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from billing.models import Bill

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample data for testing'

    def handle(self, *args, **options):
        fake = Faker()
        self.stdout.write("Starting data population...")

        # Create Admin User
        self.stdout.write("Creating admin user...")
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@hospital.com',
                'first_name': 'Hospital',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
                'password': 'admin123'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f"  ✓ Created admin user: admin / admin123")

        # Create Doctors
        self.stdout.write("Creating 15 sample doctors...")
        specializations = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'General Surgery',
                          'Gynecology', 'Dermatology', 'ENT', 'Psychiatry', 'Oncology']
        
        doctors = []
        for i in range(15):
            # Create user for doctor
            username = f"doctor{i+1}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': fake.email(),
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'password': 'password123'
                }
            )
            if created:
                user.set_password('password123')
                user.save()

            # Create doctor profile
            doctor, created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'specialization': random.choice(specializations),
                    'experience': random.randint(2, 25),
                    'phone': fake.phone_number()
                }
            )
            doctors.append(doctor)  # Add to list regardless of creation
            if created:
                self.stdout.write(f"  ✓ Created doctor: {user.first_name} {user.last_name}")

        # Create 50 Patients
        self.stdout.write("Creating 50 sample patients...")
        patients = []
        for i in range(50):
            patient = Patient.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
                gender=random.choice(['M', 'F', 'O']),
                address=fake.address(),
                city=fake.city(),
                medical_history=fake.sentence(nb_words=10) if random.choice([True, False]) else None,
                allergies=fake.word() if random.choice([True, False]) else None
            )
            patients.append(patient)
            if (i + 1) % 10 == 0:
                self.stdout.write(f"  ✓ Created {i + 1} patients")

        # Create Appointments
        self.stdout.write("Creating sample appointments...")
        appointment_count = 0
        for patient in patients[:30]:  # Create appointments for 30 patients
            num_appointments = random.randint(1, 3)
            for _ in range(num_appointments):
                doctor = random.choice(doctors)
                appointment_date = timezone.now() + timedelta(days=random.randint(-60, 30))
                
                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    appointment_date=appointment_date,
                    reason=fake.sentence(nb_words=8),
                    status=random.choice(['scheduled', 'completed', 'cancelled']),
                    notes=fake.sentence(nb_words=12) if random.choice([True, False]) else None
                )
                appointment_count += 1

        self.stdout.write(f"  ✓ Created {appointment_count} appointments")

        # Create Bills
        self.stdout.write("Creating sample bills...")
        bill_count = 0
        for patient in patients[:40]:  # Create bills for 40 patients
            num_bills = random.randint(1, 5)
            for _ in range(num_bills):
                issue_date = timezone.now() - timedelta(days=random.randint(0, 90))
                
                bill = Bill.objects.create(
                    patient=patient,
                    appointment=random.choice(
                        Appointment.objects.filter(patient=patient)
                    ) if Appointment.objects.filter(patient=patient).exists() else None,
                    amount=round(random.uniform(100, 5000), 2),
                    description=fake.sentence(nb_words=10),
                    status=random.choice(['pending', 'paid', 'overdue']),
                    due_date=issue_date + timedelta(days=30),
                    paid_date=issue_date + timedelta(days=random.randint(1, 30)) 
                              if random.choice([True, False]) else None
                )
                bill_count += 1

        self.stdout.write(f"  ✓ Created {bill_count} bills")

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Successfully populated database!\n'
            f'  • Doctors: 15\n'
            f'  • Patients: 50\n'
            f'  • Appointments: {appointment_count}\n'
            f'  • Bills: {bill_count}\n'
            f'\nLogin Credentials:\n'
            f'  ADMIN:\n'
            f'    Username: admin\n'
            f'    Password: admin123\n'
            f'\n  DOCTOR (Any from 1-15):\n'
            f'    Username: doctor1 (or doctor2, doctor3... doctor15)\n'
            f'    Password: password123\n'
        ))
