from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Teacher, Student, User, Profile

# Signal handlers
@receiver(post_save, sender=User)
def manage_user_profiles(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if instance.user_type == "Instructor":
            Teacher.objects.create(user=instance)
        elif instance.user_type == "Student":
            Student.objects.create(user=instance)
    else:
        instance.profile.save()
        if hasattr(instance, 'teacher'):
            instance.teacher.save()
        elif hasattr(instance, 'student'):
            instance.student.save()
