import datetime
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from .models import PortfolioModel


class PortfolioViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.portfolio_data = {
            "bio": "This is a test bio",
            "location": "Test City",
            "website": "https://example.com",
            "birth_date": datetime.date.today(),
            "linkedin_url": "https://linkedin.com/testuser",
            "github_url": "https://github.com/testuser",
            "kaggle_url": "https://kaggle.com/testuser",
            "google_scholar_url": "https://scholar.google.com/testuser"
        }

        self.portfolio = PortfolioModel.objects.create(user_id=self.user, **self.portfolio_data)

    def test_get_portfolios_no_id(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('portfolio-list'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_get_single_portfolio(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('portfolio-detail', kwargs={'id': self.portfolio.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], self.portfolio_data['bio'])

    def test_get_portfolio_not_found(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('portfolio-detail', kwargs={'id': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_portfolio(self):
        User.objects.create_user(username='anotheruser2', password='anotherpass')
        self.client.login(username='anotheruser2', password='anotherpass')
        updated_data = self.portfolio_data.copy()
        updated_data['bio'] = "Updated test bio"
        updated_data['location'] = 'Another test city'
        response = self.client.post(reverse('portfolio-list'), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['bio'], updated_data['bio'])

    def test_update_portfolio(self):
        self.client.login(username='testuser', password='testpass')
        updated_data = self.portfolio_data.copy()
        updated_data['bio'] = "Updated test bio"

        response = self.client.put(reverse('portfolio-detail', kwargs={'id': self.portfolio.id}), updated_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], updated_data['bio'])

    def test_update_portfolio_unauthorized(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpass')
        another_portfolio = PortfolioModel.objects.create(user_id=another_user, **self.portfolio_data)

        response = self.client.put(reverse('portfolio-detail', kwargs={'id': another_portfolio.id}),
                                   self.portfolio_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_portfolio(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse("portfolio-detail"), kwargs={'id': self.portfolio.id})
        self.assertTrue(response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_204_NO_CONTENT)
