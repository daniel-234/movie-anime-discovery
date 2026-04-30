from django.contrib.auth.models import User
from django.test import TestCase

from account.models import Profile


class ProfileSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pass1234!")

    def test_profile_exists_for_user(self):
        assert self.user.username == "alice"
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_profile_bio(self):
        self.user.profile.bio = "Movie lover"
        self.user.save()

        self.user.refresh_from_db()
        assert self.user.profile.bio != "Movie lover"

    def test_profile_delete(self):
        self.user.delete()

        self.assertTrue(Profile.objects.count() == 0)
