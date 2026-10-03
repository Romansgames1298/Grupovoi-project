from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def test_register_creates_user_profile_with_user_role(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'testuser2',
                'email': 'testuser2@example.com',
                'first_name': 'Тест',
                'last_name': 'Користувач',
                'password1': 'Strongpass123!',
                'password2': 'Strongpass123!',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get(username='testuser2')
        self.assertEqual(user.profile.role, 'user')
        self.assertIn('user', [group.name for group in user.groups.all()])

    def test_seed_roles_creates_admin_accounts(self):
        call_command('seed_roles')
        user = get_user_model().objects.filter(username='teacher').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.profile.role, 'admin')
