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
        # self.factory = APIRequestFactory()
        # self.view = PostListCreateView.as_view()
        self.url = reverse("list_posts")
        # self.user = User.objects.create(
        #     username = "janedoe",
        #     email = "janedoe@app.com",
        #     password = "password@1234"
        # )

    def authenticate(self):
        self.client.post(
            reverse('signup'),
            {
                "email": "janedoe@app.com",
                "password": "password@1234",
                "username": "janedoe",
            },
        )

        response = self.client.post(
            reverse('login'),
            {
               "email": "janedoe@app.com",
               "password": "password@1234", 
            }
            )
        # print(response.data)

        token = response.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')

    def test_list_posts(self):
        # using apifactory
        # request = self.factory.get(self.url)
        # response = self.view(request)

        # using apiclient
        response = self.client.get(self.url)

        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['count'], 0)
        # self.assertEqual(response.data["results"], [])

    def test_post_creation(self):
        sample_post = {
            "title": "Sample post",
            "content": "Sample content"
        }
        # request = self.factory.post(self.url, sample_post)
        # request.user = self.user
        # response = self.view(request)

        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # using api client
        self.authenticate()
        response = self.client.post(self.url, sample_post)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], sample_post['title'])

