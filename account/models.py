from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    @transaction.atomic
    def update(self, user_data: dict, profile_data: dict) -> None:
        for field, value in user_data.items():
            setattr(self.user, field, value)
        for field, value in profile_data.items():
            setattr(self, field, value)
        self.user.save()
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
