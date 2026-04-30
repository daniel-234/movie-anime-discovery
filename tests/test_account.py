from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

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


class SignupViewTest(TestCase):
    def setUp(self):
        data = {
            "username": "newUser",
            "password1": "Str0ngPass!99",
            "password2": "Str0ngPass!99",
        }
        self.client.post(reverse("signup"), data)

    def test_get_method(self):
        response = self.client.get(reverse("signup"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_post_method(self):
        self.assertTrue(User.objects.filter(username="newUser").exists())
