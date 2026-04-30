from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account.models import Profile


class ProfileSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pass1234!")

    def test_user_object_creation_also_creates_related_profile(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_deleting_user_also_deletes_related_profile_entry(self):
        self.user.delete()
        self.assertTrue(Profile.objects.count() == 0)

    def test_deleting_profile_user_remains(self):
        # cascade delete means you delete the related model
        # but we learned that the user is the parent and the profile
        # is the child, so deleting the profile should not delete the user
        self.user.profile.delete()
        self.assertTrue(User.objects.count() == 1)

    def test_update_profile(self):
        self.user.profile.update(
            user_data={"username": "bob"}, profile_data={"bio": "Movie lover"}
        )
        assert self.user.username == "bob"
        assert self.user.profile.bio == "Movie lover"


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
