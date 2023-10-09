from askbot.tests.utils import AskbotTestCase
from askbot.models import User

class UnsubscribeUserTests(AskbotTestCase):
    def test_unsubscribe_url_for_missing_user(self):
        user = User.objects.create_user('user', email='user@example.com')
        unsub_url = user.get_unsubscribe_url()
        user.delete()
        response = self.client.get(unsub_url)
        self.assertEqual(response.status_code, 200)
