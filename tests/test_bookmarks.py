import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from media.models import Anime, Manga, Movie, SavedAnime, SavedManga, SavedMovie
from media.views import _resolve

CONTENT_TYPES = [
    ("movie", Movie, SavedMovie, "movie", "fight-club", "Fight Club"),
    ("anime", Anime, SavedAnime, "anime", "cowboy-bebop", "Cowboy Bebop"),
    ("manga", Manga, SavedManga, "manga", "berserk", "Berserk"),
]


@pytest.fixture
def logged_in_user(db, client):
    user = User.objects.create_user(username="bookmarker", password="pass1234!")
    client.force_login(user)
    return user


@pytest.fixture
def content_item(db, content_model, slug, title):
    return content_model.objects.create(slug=slug, title=title)


@pytest.mark.parametrize(
    "content_type, content_model, saved_model, fk_name, slug, title", CONTENT_TYPES
)
def test_post_creates_bookmark_for_unbookmarked_item(
    logged_in_user, client, content_item, content_type, saved_model, fk_name
):
    assert not saved_model.objects.filter(
        user=logged_in_user, **{fk_name: content_item}
    ).exists()
    toggle_url = reverse(
        "media:toggle_bookmark",
        kwargs={"content_type": content_type, "slug": content_item.slug},
    )
    response = client.post(toggle_url)
    assert response.status_code == 200
    assert saved_model.objects.filter(
        user=logged_in_user, **{fk_name: content_item}
    ).exists()


@pytest.mark.parametrize(
    "content_type, content_model, saved_model, fk_name, slug, title", CONTENT_TYPES
)
def test_post_removes_bookmark_when_already_bookmarked(
    logged_in_user, client, content_item, content_type, saved_model, fk_name
):
    saved_model.objects.create(user=logged_in_user, **{fk_name: content_item})
    toggle_url = reverse(
        "media:toggle_bookmark",
        kwargs={"content_type": content_type, "slug": content_item.slug},
    )
    response = client.post(toggle_url)
    assert response.status_code == 200
    assert not saved_model.objects.filter(
        user=logged_in_user, **{fk_name: content_item}
    ).exists()


@pytest.mark.parametrize(
    "content_type, content_model, saved_model, fk_name, slug, title", CONTENT_TYPES
)
def test_post_toggles_back_and_forth(
    logged_in_user, client, content_item, content_type, saved_model, fk_name
):
    """Three POSTs round-trip cleanly: absent → present → absent → present."""
    toggle_url = reverse(
        "media:toggle_bookmark",
        kwargs={"content_type": content_type, "slug": content_item.slug},
    )
    for expected_to_exist in (True, False, True):
        client.post(toggle_url)
        actual = saved_model.objects.filter(
            user=logged_in_user, **{fk_name: content_item}
        ).exists()
        assert actual == expected_to_exist


@pytest.mark.parametrize(
    "content_type, expected",
    [
        ("movie", (Movie, SavedMovie, "movie")),
        ("anime", (Anime, SavedAnime, "anime")),
        ("manga", (Manga, SavedManga, "manga")),
    ],
)
def test_resolve_returns_correct_tuple(content_type, expected):
    assert _resolve(content_type) == expected
