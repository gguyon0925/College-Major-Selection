# python manage.py test users

from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import Interest, UserProfile
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .serializers import CustomUserSerializer
from django.urls import resolve
from .views import CustomUserViewSet

User = get_user_model()


class UserModelTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='pass')
        user.bio = "This is a bio."
        user.job_security_preference = 'HIGH'
        user.expected_income = 100000
        user.save()

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.bio, "This is a bio.")
        self.assertTrue(user.check_password('pass'))
        self.assertEqual(user.job_security_preference, 'HIGH')
        self.assertEqual(user.expected_income, 100000)


class UserProfileTests(TestCase):

    def test_create_user_profile(self):
        user = User.objects.create_user(username='testuser', password='pass')
        profile = UserProfile.objects.create(user=user)
        interest = Interest.objects.create(name="Python")
        profile.interests.add(interest)

        self.assertEqual(profile.user.username, 'testuser')
        self.assertTrue(profile.interests.filter(name="Python").exists())


class CustomUserViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

    def test_user_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('customuser-detail', kwargs={'pk': self.user.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_unauthorized_user_retrieve(self):
        response = self.client.get(
            reverse('customuser-detail', kwargs={'pk': self.user.pk}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('customuser-detail', kwargs={'pk': self.user.pk})
        data = {'bio': 'Updated bio.', 'job_security_preference': 'MEDIUM'}
        response = self.client.patch(url, data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.bio, 'Updated bio.')
        self.assertEqual(self.user.job_security_preference, 'MEDIUM')

    def test_user_list(self):
        User.objects.create_user(username='testuser2', password='pass2')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('customuser-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Adjust

    def test_user_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('customuser-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())


class CustomUserSerializerTests(TestCase):

    def test_serializer_with_empty_data(self):
        serializer = CustomUserSerializer(data={})
        self.assertFalse(serializer.is_valid())

    def test_serializer_with_valid_data(self):
        user = User.objects.create_user(
            username='testuser', password='testpass', bio="Test bio")
        serializer = CustomUserSerializer(user)

        self.assertEqual(serializer.data['username'], 'testuser')
        self.assertEqual(serializer.data['bio'], 'Test bio')


class UrlsTests(TestCase):

    def test_user_detail_url(self):
        view = resolve('/api/users/1/')
        self.assertEqual(view.func.__name__, CustomUserViewSet.as_view(
            {'get': 'retrieve'}).__name__)
