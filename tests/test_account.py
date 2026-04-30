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
        self.data = {
            "username": "newUser",
            "password1": "Str0ngPass!99",
            "password2": "Str0ngPass!99",
        }

    def test_get_method_to_signup(self):
        response = self.client.get(reverse("signup"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_profile_exists_after_signup(self):
        response = self.client.post(reverse("signup"), self.data)
        assert response.status_code == 302
        assert response["Location"] == reverse("login")
        self.assertTrue(User.objects.filter(username="newUser").exists())
        self.assertTrue(Profile.objects.count() == 1)

    def test_passwords_do_not_match_in_signup_post(self):
        self.data["password2"] = "stringPass!00"
        response = self.client.post(reverse("signup"), self.data)
        assert response.status_code == 200
        assert response.status_code != 302
        self.assertTrue(User.objects.count() == 0)


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dashuser", password="pass1234!")

    def test_anonymous_client_gets_redirected_to_login_page(self):
        response = self.client.get(reverse("dashboard"))
        assert response.status_code == 302
        # Django's @login_required (and LoginRequiredMixin) appends a
        # ?next=... query string to the login URL so the user can be
        # sent back to where they were trying to go after logging in
        expected = f"{reverse('login')}?next={reverse('dashboard')}"
        assert response["Location"] == expected

    def test_logged_in_client_gets_rendered_the_dashboard(self):
        self.assertTrue(self.client.login(username="dashuser", password="pass1234!"))
        response = self.client.get(reverse("dashboard"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "account/dashboard.html")

    def test_that_cache_control_header_contains_no_store(self):
        self.client.login(username="dashuser", password="pass1234!")
        response = self.client.get(reverse("dashboard"))
        header = response.get("Cache-Control", "")
        self.assertIn("no-store", header)
