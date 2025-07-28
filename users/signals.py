from django.dispatch import receiver
from .models import Profile, User
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile =  Profile.objects.create(user=instance)
       profile.role = "User"
       profile.gender = "Male"
       profile.save()