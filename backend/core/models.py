from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    given_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_description = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"{self.given_name} {self.surname}"

class Caregiver(models.Model):
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    CAREGIVING_TYPE_CHOICES = [("Babysitter", "Babysitter"), ("Elderly Care", "Elderly Care"), ("Playmate", "Playmate")]

    caregiver_user = models.OneToOneField(User, on_delete=models.CASCADE, db_column="caregiver_user_id", primary_key=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    caregiving_type = models.CharField(max_length=20, choices=CAREGIVING_TYPE_CHOICES)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = "caregiver"

    def __str__(self):
        return f"Caregiver: {self.caregiver_user.given_name} {self.caregiver_user.surname}"

class Member(models.Model):
    member_user = models.OneToOneField(User, on_delete=models.CASCADE, db_column="member_user_id", primary_key=True)
    house_rules = models.TextField(blank=True, null=True)
    dependent_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "member"

    def __str__(self):
        return f"Member: {self.member_user.given_name} {self.member_user.surname}"

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column="member_user_id")
    house_number = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    town = models.CharField(max_length=100)

    class Meta:
        db_table = "address"
        unique_together = ("member", "house_number", "street", "town")

    def __str__(self):
        return f"{self.house_number} {self.street}, {self.town}"

class Job(models.Model):
    CAREGIVING_TYPE_CHOICES = [("Babysitter", "Babysitter"), ("Elderly Care", "Elderly Care"), ("Playmate", "Playmate")]
    
    job_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column="member_user_id")
    required_caregiving_type = models.CharField(max_length=20, choices=CAREGIVING_TYPE_CHOICES)
    other_requirements = models.TextField(blank=True, null=True)
    date_posted = models.DateField()

    class Meta:
        db_table = "job"

    def __str__(self):
        return f"Job {self.job_id}"

class JobApplication(models.Model):
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, db_column="caregiver_user_id")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date_applied = models.DateField()

    class Meta:
        db_table = "job_application"
        unique_together = ("caregiver", "job")

    def __str__(self):
        return f"{self.caregiver.caregiver_user.given_name} -> Job {self.job.job_id}"

class Appointment(models.Model):
    STATUS_CHOICES = [("Pending", "Pending"), ("Accepted", "Accepted"), ("Declined", "Declined"), ("Cancelled", "Cancelled")]
    
    appointment_id = models.AutoField(primary_key=True)
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, db_column="caregiver_user_id")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column="member_user_id")
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    work_hours = models.DecimalField(max_digits=4, decimal_places=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    class Meta:
        db_table = "appointment"

    def __str__(self):
        return f"Appointment {self.appointment_id}"