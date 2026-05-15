from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from media.models import Movie, SavedMovie


class TestBookmarkToggle(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bookmarker", password="pass1234!"
        )
        self.movie = Movie.objects.create(
            slug="fight-club",
            title="Fight Club",
        )
        self.client.force_login(self.user)
        self.toggle_url = reverse(
            "media:toggle_bookmark",
            kwargs={"content_type": "movie", "slug": self.movie.slug},
        )

    def test_post_creates_bookmark_for_unbookmarked_item(self):
        self.assertFalse(
            SavedMovie.objects.filter(user=self.user, movie=self.movie).exists()
        )

        response = self.client.post(self.toggle_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            SavedMovie.objects.filter(user=self.user, movie=self.movie).exists()
        )

    def test_post_removes_bookmark_when_already_bookmarked(self):
        SavedMovie.objects.create(user=self.user, movie=self.movie)

        response = self.client.post(self.toggle_url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            SavedMovie.objects.filter(user=self.user, movie=self.movie).exists()
        )

    def test_post_toggles_back_and_forth(self):
        """Three POSTs round-trip cleanly: absent → present → absent → present."""
        for expected_to_exist in (True, False, True):
            self.client.post(self.toggle_url)
            actual = SavedMovie.objects.filter(
                user=self.user, movie=self.movie
            ).exists()
            self.assertEqual(actual, expected_to_exist)
