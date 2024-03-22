from http import HTTPStatus
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import User, EmailVerification

# Create your tests here.


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Maria',
            'last_name': 'Zat',
            'username': 'mzat',
            'password1': 'Polar33!', 'password2': 'Polar33!',
            'email': 'elena.zatykina@gmail.com',
        }
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Registration')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):

        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)
        print("Status code: ", response.status_code)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        username = self.data['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.data)
        print("Status code: ", response.status_code)

        self.assertEqual(response.status_code, HTTPStatus.OK)
