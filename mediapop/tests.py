from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from mediapop.models import Media, MediaVote
from mediapop.views import get_recommendation_scores


# Create your tests here.


class MediaVoteTest(TestCase):
    username = "testuser"
    password = "testpassword"
    pk = None

    def setUp(self):
        # Basic user
        self.user = User.objects.create_user(username=self.username, password=self.password)

        self.pk = Media.objects.create(name="Test media", media_type="vg").pk

    def test_vote_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.post(reverse("index:media_detail", args=[self.pk]),
                                    data={
            'vote': '9.3'
        })

        self.assertEqual(response.status_code, 200)

    def test_vote_anonymous_user(self):
        response = self.client.post(reverse("index:media_detail", args=[self.pk]),
                                    data={
                                        'vote': '9.3'
                                    })

        self.assertEqual(response.status_code, 302)


class RecommendationSystemTest(TestCase):
    username = "testuser"
    password = "testpassword"

    def setUp(self):
        # Basic user
        self.user = User.objects.create_user(username=self.username, password=self.password)

        n_tot_media = 30
        self.media_types = {
            "vg": 1,
            "f": 3,
            "tv": 4,
            "a": 2
        }

        for i in range(n_tot_media):
            mt = i % 4

            Media.objects.create(name=f"media{i}", media_type=list(self.media_types.keys())[mt])

        for key, val in self.media_types.items():
            filtered = Media.objects.filter(media_type=key)

            for i in range(val):
                MediaVote.objects.create(user=self.user, media=filtered[i], vote="8")

    def test_recommended_media(self):
        self.client.login(username=self.username, password=self.password)

        request = HttpRequest()
        request.user = self.user

        recommended_scores = get_recommendation_scores(request)
        result = [item[0] for item in recommended_scores]
        expected_result = [item[0] for item in sorted(self.media_types.items(), key=lambda item: item[1], reverse=True)]

        self.assertEqual(expected_result, result)

