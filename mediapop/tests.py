from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from mediapop.models import Media


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

        print(response.status_code)

        self.assertEqual(response.status_code, 302)

        print(response.url)
