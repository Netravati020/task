from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class UserActivityLogTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')
        self.log_url = "/api/activity/logs/"
        self.data = {
            "action": "LOGIN",
            "metadata": {"ip": "127.0.0.1"},
            "status": "PENDING"
        }

    def test_create_log(self):
        response = self.client.post(self.log_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_logs(self):
        self.client.post(self.log_url, self.data, format='json')
        response = self.client.get(self.log_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_update_status(self):
        response = self.client.post(self.log_url, self.data, format='json')
        log_id = response.data['id']
        patch_url = f"{self.log_url}{log_id}/update-status/"
        response = self.client.patch(patch_url, {"status": "DONE"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "DONE")

    def test_filter_by_action(self):
        self.client.post(self.log_url, self.data, format='json')
        response = self.client.get(self.log_url + "?action=LOGIN")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(log['action'] == 'LOGIN' for log in response.data))
