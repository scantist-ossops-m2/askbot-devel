from django.urls import reverse
from bs4 import BeautifulSoup
from askbot.tests.utils import AskbotTestCase
from askbot.models import User

class UnsubscribeUserTests(AskbotTestCase):
    def test_unsubscribe_url_for_missing_user(self):
        user = User.objects.create_user('user', email='user@example.com')
        unsub_url = user.get_unsubscribe_url()
        user.delete()
        response = self.client.get(unsub_url)
        self.assertEqual(response.status_code, 200)

    def test_unsubscribe_user(self):
        user = User.objects.create_user('user', email='user@example.com')
        self.assertTrue(user.notification_subscriptions.exclude(frequency='n').exists())
        unsub_url = user.get_unsubscribe_url()

        #load the unsubscribe page
        response = self.client.get(unsub_url)
        soup = BeautifulSoup(response.content)
        form = soup.find('form', attrs={'action': reverse('user_unsubscribe')})
        #collect the unsubscribe parameters from the page
        csrftoken = form.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']
        email = form.find('input', attrs={'name': 'email'})['value']
        key = form.find('input', attrs={'name': 'key'})['value']

        #post the unsubscribe form
        post_data = {
            'csrfmiddlewaretoken': csrftoken,
            'email': email,
            'key': key,
        }
        response = self.client.post(reverse('user_unsubscribe'), data=post_data)
        user = User.objects.get(email='user@example.com')
        self.assertFalse(user.notification_subscriptions.exclude(frequency='n').exists())
