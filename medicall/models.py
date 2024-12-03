from django.db import models
from django.core.validators import RegexValidator

class Appointment(models.Model):
    phone_validator = RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits.')
    
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[phone_validator])
    date = models.DateTimeField()  # Or use DateField() if you want to store only the date
    department = models.CharField(max_length=50)  # Increased length
    doctor = models.CharField(max_length=50)  # Increased length
    message = models.TextField()
    action = models

    def __str__(self):
        return f"{self.name} - {self.date.strftime('%Y-%m-%d %H:%M')}"


class UploadedImage(models.Model):
    title = models.CharField(max_length=100)  # Title for the image
    image = models.ImageField(upload_to='uploaded_images/')  # Save images to this folder

    def __str__(self):
        return self.title