from django.contrib.auth.models import User
from django.test import TestCase

from account.models import Profile


class ProfileSignalTest(TestCase):
    def test_profile_exixts_for_user(self):
        user = User.objects.create_user("alice", password="pass1234!")
        assert user.username == "alice"
        assert Profile.objects.filter(user=user).exists()

    def test_profile_bio(self):
        user = User.objects.create_user("alice", password="pass1234!")
        user.profile.bio = "Movie lover"
        user.save()

        user.refresh_from_db()
        assert user.profile.bio != "Movie lover"

    def test_profile_delete(self):
        user = User.objects.create_user("alice", password="pass1234!")
        profile_primary_key = user.profile.pk

        user.delete()

        self.assertFalse(Profile.objects.filter(pk=profile_primary_key).exists())
