from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Ad, Category, ExchangeProposal

User = get_user_model()

class AdsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(title="TestCategory")
        self.ad = Ad.objects.create(
            title="Test Ad",
            description="Test Description",
            category=self.category,
            condition=Ad.Condition.NEW,
            user=self.user
        )
        self.exchange = ExchangeProposal.objects.create(
            ad_sender=self.ad,
            ad_receiver=self.ad,
            status=ExchangeProposal.Status.WAIT
        )

    def test_home_view(self):
        url = reverse('ads:home')  # замените на актуальное имя URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ads', response.context)

    def test_profile_view_requires_login(self):
        url = reverse('ads:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # редирект на логин

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ads', response.context)

    def test_ad_create_view(self):
        url = reverse('ads:create')  # замените на актуальное имя URL
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {
            'title': 'New Ad',
            'description': 'New Description',
            'category': self.category.id,
            'condition': Ad.Condition.NEW,
        })
        self.assertEqual(response.status_code, 302)  # редирект после успешного создания

    def test_ad_detail_view(self):
        url = reverse('ads:detail', kwargs={'pk': self.ad.pk})  # замените на актуальное имя URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ad'], self.ad)

    def test_ad_update_view_permission(self):
        url = reverse('ads:update', kwargs={'pk': self.ad.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_ad_view_permission(self):
        url = reverse('ads:delete', kwargs={'pk': self.ad.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_searching_view(self):
        url = reverse('ads:searching')
        response = self.client.get(url, {'searching': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('ads', response.context)

    def test_exchange_list_view(self):
        url = reverse('ads:list_ex')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ads', response.context)

