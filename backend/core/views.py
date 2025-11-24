from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.contrib import messages
from .models import User, Caregiver, Member, Job, Appointment, JobApplication, Address

def index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM caregiver")
        caregiver_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM member")
        member_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM job")
        job_count = cursor.fetchone()[0]
    
    context = {
        'user_count': user_count,
        'caregiver_count': caregiver_count,
        'member_count': member_count,
        'job_count': job_count,
    }
    return render(request, 'index.html', context)

# User Views
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_detail(request, pk):
    user = get_object_or_404(User, user_id=pk)
    return render(request, 'users/user_detail.html', {'user': user})

def user_create(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO user (email, given_name, surname, city, phone_number, profile_description, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [
                request.POST['email'],
                request.POST['given_name'],
                request.POST['surname'],
                request.POST['city'],
                request.POST.get('phone_number', ''),
                request.POST.get('profile_description', ''),
                request.POST['password']
            ])
        messages.success(request, 'User created successfully!')
        return redirect('user_list')
    return render(request, 'users/user_form.html')

def user_update(request, pk):
    user = get_object_or_404(User, user_id=pk)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE user 
                SET email=%s, given_name=%s, surname=%s, city=%s, 
                    phone_number=%s, profile_description=%s, password=%s
                WHERE user_id=%s
            """, [
                request.POST['email'],
                request.POST['given_name'],
                request.POST['surname'],
                request.POST['city'],
                request.POST.get('phone_number', ''),
                request.POST.get('profile_description', ''),
                request.POST['password'],
                pk
            ])
        messages.success(request, 'User updated successfully!')
        return redirect('user_list')
    return render(request, 'users/user_form.html', {'user': user})

def user_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM user WHERE user_id = %s", [pk])
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': get_object_or_404(User, user_id=pk)})

# Caregiver Views
def caregiver_list(request):
    caregivers = Caregiver.objects.all()
    return render(request, 'caregivers/caregiver_list.html', {'caregivers': caregivers})

def caregiver_detail(request, pk):
    caregiver = get_object_or_404(Caregiver, caregiver_user_id=pk)
    return render(request, 'caregivers/caregiver_detail.html', {'caregiver': caregiver})

def caregiver_create(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate)
                VALUES (%s, %s, %s, %s, %s)
            """, [
                request.POST['caregiver_user_id'],
                request.POST.get('photo', ''),
                request.POST['gender'],
                request.POST['caregiving_type'],
                request.POST['hourly_rate']
            ])
        messages.success(request, 'Caregiver created successfully!')
        return redirect('caregiver_list')
    return render(request, 'caregivers/caregiver_form.html')

def caregiver_update(request, pk):
    caregiver = get_object_or_404(Caregiver, caregiver_user_id=pk)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE caregiver 
                SET photo=%s, gender=%s, caregiving_type=%s, hourly_rate=%s
                WHERE caregiver_user_id=%s
            """, [
                request.POST.get('photo', ''),
                request.POST['gender'],
                request.POST['caregiving_type'],
                request.POST['hourly_rate'],
                pk
            ])
        messages.success(request, 'Caregiver updated successfully!')
        return redirect('caregiver_list')
    return render(request, 'caregivers/caregiver_form.html', {'caregiver': caregiver})

def caregiver_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM caregiver WHERE caregiver_user_id = %s", [pk])
        messages.success(request, 'Caregiver deleted successfully!')
        return redirect('caregiver_list')
    return render(request, 'caregivers/caregiver_confirm_delete.html', {'caregiver': get_object_or_404(Caregiver, caregiver_user_id=pk)})

# Member Views
def member_list(request):
    members = Member.objects.all()
    return render(request, 'members/member_list.html', {'members': members})

def member_detail(request, pk):
    member = get_object_or_404(Member, member_user_id=pk)
    return render(request, 'members/member_detail.html', {'member': member})

def member_create(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO member (member_user_id, house_rules, dependent_description)
                VALUES (%s, %s, %s)
            """, [
                request.POST['member_user_id'],
                request.POST.get('house_rules', ''),
                request.POST.get('dependent_description', '')
            ])
        messages.success(request, 'Member created successfully!')
        return redirect('member_list')
    return render(request, 'members/member_form.html')

def member_update(request, pk):
    member = get_object_or_404(Member, member_user_id=pk)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE member 
                SET house_rules=%s, dependent_description=%s
                WHERE member_user_id=%s
            """, [
                request.POST.get('house_rules', ''),
                request.POST.get('dependent_description', ''),
                pk
            ])
        messages.success(request, 'Member updated successfully!')
        return redirect('member_list')
    return render(request, 'members/member_form.html', {'member': member})

def member_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM member WHERE member_user_id = %s", [pk])
        messages.success(request, 'Member deleted successfully!')
        return redirect('member_list')
    return render(request, 'members/member_confirm_delete.html', {'member': get_object_or_404(Member, member_user_id=pk)})

# Job Views
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, job_id=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

def job_create(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO job (member_user_id, required_caregiving_type, other_requirements, date_posted)
                VALUES (%s, %s, %s, %s)
            """, [
                request.POST['member_user_id'],
                request.POST['required_caregiving_type'],
                request.POST.get('other_requirements', ''),
                request.POST['date_posted']
            ])
        messages.success(request, 'Job created successfully!')
        return redirect('job_list')
    return render(request, 'jobs/job_form.html')

def job_update(request, pk):
    job = get_object_or_404(Job, job_id=pk)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE job 
                SET member_user_id=%s, required_caregiving_type=%s, other_requirements=%s, date_posted=%s
                WHERE job_id=%s
            """, [
                request.POST['member_user_id'],
                request.POST['required_caregiving_type'],
                request.POST.get('other_requirements', ''),
                request.POST['date_posted'],
                pk
            ])
        messages.success(request, 'Job updated successfully!')
        return redirect('job_list')
    return render(request, 'jobs/job_form.html', {'job': job})

def job_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM job WHERE job_id = %s", [pk])
        messages.success(request, 'Job deleted successfully!')
        return redirect('job_list')
    return render(request, 'jobs/job_confirm_delete.html', {'job': get_object_or_404(Job, job_id=pk)})

# Appointment Views
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, appointment_id=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

def appointment_create(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO appointment (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [
                request.POST['caregiver_user_id'],
                request.POST['member_user_id'],
                request.POST['appointment_date'],
                request.POST['appointment_time'],
                request.POST['work_hours'],
                request.POST['status']
            ])
        messages.success(request, 'Appointment created successfully!')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_form.html')

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, appointment_id=pk)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE appointment 
                SET caregiver_user_id=%s, member_user_id=%s, appointment_date=%s, 
                    appointment_time=%s, work_hours=%s, status=%s
                WHERE appointment_id=%s
            """, [
                request.POST['caregiver_user_id'],
                request.POST['member_user_id'],
                request.POST['appointment_date'],
                request.POST['appointment_time'],
                request.POST['work_hours'],
                request.POST['status'],
                pk
            ])
        messages.success(request, 'Appointment updated successfully!')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_form.html', {'appointment': appointment})

def appointment_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM appointment WHERE appointment_id = %s", [pk])
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': get_object_or_404(Appointment, appointment_id=pk)})

# Job Application Views
def job_application_list(request):
    job_applications = JobApplication.objects.all()
    return render(request, 'job_applications/job_application_list.html', {'job_applications': job_applications})

def job_application_detail(request, caregiver_id, job_id):
    job_application = get_object_or_404(
        JobApplication,
        caregiver_id=caregiver_id,   # имя поля в модели -> caregiver
        job_id=job_id
    )
    return render(
        request,
        "job_applications/job_application_detail.html",
        {"job_application": job_application},
    )

def job_application_create(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO job_application (caregiver_user_id, job_id, date_applied)
                VALUES (%s, %s, %s)
            """, [
                request.POST['caregiver_user_id'],
                request.POST['job_id'],
                request.POST['date_applied']
            ])
        messages.success(request, 'Job application created successfully!')
        return redirect('job_application_list')
    return render(request, 'job_applications/job_application_form.html')

def job_application_delete(request, caregiver_id, job_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM job_application WHERE caregiver_user_id = %s AND job_id = %s", [caregiver_id, job_id])
        messages.success(request, 'Job application deleted successfully!')
        return redirect('job_application_list')
    job_application = get_object_or_404(
        JobApplication,
        caregiver_id=caregiver_id,
        job_id=job_id,
    )
    return render(request, 'job_applications/job_application_confirm_delete.html', {'job_application': job_application})

def job_application_update(request, caregiver_id, job_id):
    job_application = get_object_or_404(
        JobApplication,
        caregiver_id=caregiver_id,
        job_id=job_id,
    )
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE job_application
                SET date_applied = %s
                WHERE caregiver_user_id = %s AND job_id = %s
                """,
                [
                    request.POST["date_applied"],
                    caregiver_id,
                    job_id,
                ],
            )
        messages.success(request, "Job application updated successfully!")
        return redirect("job_application_list")

    return render(
        request,
        "job_applications/job_application_form.html",
        {"job_application": job_application},
    )


def address_list(request):
    addresses = Address.objects.select_related("member__member_user").all()
    return render(request, "addresses/address_list.html", {"addresses": addresses})


def address_detail(request, pk):
    address = get_object_or_404(Address, id=pk)
    return render(request, "addresses/address_detail.html", {"address": address})


def address_create(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO address (member_user_id, house_number, street, town)
                VALUES (%s, %s, %s, %s)
                """,
                [
                    request.POST["member_user_id"],
                    request.POST["house_number"],
                    request.POST["street"],
                    request.POST["town"],
                ],
            )
        messages.success(request, "Address created successfully!")
        return redirect("address_list")

    return render(request, "addresses/address_form.html")


def address_update(request, pk):
    address = get_object_or_404(Address, id=pk)
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE address
                SET member_user_id=%s, house_number=%s, street=%s, town=%s
                WHERE id=%s
                """,
                [
                    request.POST["member_user_id"],
                    request.POST["house_number"],
                    request.POST["street"],
                    request.POST["town"],
                    pk,
                ],
            )
        messages.success(request, "Address updated successfully!")
        return redirect("address_list")

    return render(request, "addresses/address_form.html", {"address": address})


def address_delete(request, pk):
    address = get_object_or_404(Address, id=pk)
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM address WHERE id = %s", [pk])
        messages.success(request, "Address deleted successfully!")
        return redirect("address_list")

    return render(
        request,
        "addresses/address_confirm_delete.html",
        {"address": address},
    )
