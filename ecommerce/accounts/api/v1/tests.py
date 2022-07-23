from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

User = get_user_model()


class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "email": "test2@example.com",
            "phone_number": "09333456789",
            "first_name": "Dave",
            "last_name": "Elder",
            "password": "some_str_passwd",
            "password2": "some_str_passwd",
        }
        self.test_user = User.objects.create_user(
            email="testing@test.com",
            phone_number="09122233456",
            first_name="test",
            last_name="tested",
            password="some_strong_password",
            passed_phone_number_verification=True,
        )
        return super().setUp()

    def test_registration(self):
        response = self.client.post("/api-auth/register/", self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_email(self):
        response = self.client.post(
            "/api-auth/login/",
            {"email": self.test_user.email, "password": "some_strong_password"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_phone_number(self):
        response = self.client.post(
            "/api-auth/login/",
            {"email": self.test_user.phone_number, "password": "some_strong_password"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_profile_unauthorized(self):
        profile_pk = self.test_user.profile.pk
        res = self.client.get(reverse("user_profile", kwargs={"pk": profile_pk}))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_profile_authorized(self):
        response = self.client.post(
            "/api-auth/login/",
            {"email": self.test_user.email, "password": "some_strong_password"},
        )
        profile_pk = self.test_user.profile.pk
        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        res = self.client.get(reverse("user_profile", kwargs={"pk": profile_pk}))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_not_allowed_on_profile_endpoint(self):
        response = self.client.post(
            "/api-auth/login/",
            {"email": self.test_user.email, "password": "some_strong_password"},
        )
        profile_pk = self.test_user.profile.pk
        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        res = self.client.post(reverse("user_profile", kwargs={"pk": profile_pk}), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        response = self.client.post(
            "/api-auth/login/",
            {"email": self.test_user.email, "password": "some_strong_password"},
        )
        profile_pk = self.test_user.profile.pk
        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        payload = {"bio": "Some Fancy Bio"}

        res = self.client.put(
            reverse("user_profile", kwargs={"pk": profile_pk}), payload
        )

        self.test_user.refresh_from_db()

        self.assertEqual(self.test_user.profile.bio, payload["bio"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
