from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

USER_TYPE = [
    ("Instructor", "Instructor"),
    ("Student", "Student")
]

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    institution = models.CharField(max_length=300)
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default="None")
    otp = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='user_folder', default='default_user.jpg', null=True, blank=True)
    full_name = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)