from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status
from .views import PostListCreateView
from django.contrib.auth import get_user_model

User = get_user_model()

class HelloWorldTestCase(APITestCase):
    def test_hello_world(self):
        response = self.client.get(reverse("posts_home"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Hello World")

class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PostListCreateView.as_view()
        self.url = reverse("list_posts")

    def test_list_posts(self):
        request = self.factory.get(self.url)
        response = self.view(request)

        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['count'], 0)
        # self.assertEqual(response.data["results"], [])
