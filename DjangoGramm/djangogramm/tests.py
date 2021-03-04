from django.test import TestCase


# Create your tests here.
class YourTestClass(TestCase):

    def setUp(self):
        pass

    def test_index(self):
        index_resp = str(self.client.get('').content)
        self.assertIn(
            '<h5 class="card-title">Log in</h5>',
            index_resp,
            )
        self.assertEqual(
            index_resp,
            str(self.client.get('login/').content),
            )

    def test_registration_page(self):
        self.assertIn(
            '<p>After registration, an individually generated link will be sent to your specified email address.</p>',
            str(self.client.get('registration/').content),
            )
