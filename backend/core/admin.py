from django.contrib import admin
from .models import (
    User,
    Caregiver,
    Member,
    Address,
    Job,
    JobApplication,
    Appointment,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "given_name", "surname", "email", "city")
    search_fields = ("given_name", "surname", "email", "city")


@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
    list_display = ("caregiver_user", "gender", "caregiving_type", "hourly_rate")
    list_filter = ("caregiving_type", "gender")


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("member_user",)
    search_fields = ("member_user__given_name", "member_user__surname")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("member", "house_number", "street", "town")
    list_filter = ("town", "street")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("job_id", "member", "required_caregiving_type", "date_posted")
    list_filter = ("required_caregiving_type", "date_posted")


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("caregiver", "job", "date_applied")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "appointment_id",
        "caregiver",
        "member",
        "appointment_date",
        "appointment_time",
        "work_hours",
        "status",
    )
    list_filter = ("status", "appointment_date")
