from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.test import TestCase
from django.utils.lorem_ipsum import words

from .models import Account, Picture, Post


# Create your tests here.
class YourTestClass(TestCase):

    def setUp(self):
        self.account = Account.objects.create(
            id=967103409,
            email='test@user.com',
            password='password',
            first_name='Максим',
            last_name='Шаврин',
            about_yourself=words(16)
        )
        self.avatar = Picture(
            picture_itself=SimpleUploadedFile('image.jpeg', b'', 'image/gpeg'),
            avatar_of=self.account,
        ).save()
        for item in range(7):
            Post(text=words(16), author=self.account).save()

    def test_index_login_page(self):
        index_resp = str(self.client.get('/').content)
        self.assertIn('<h5 class="card-title">Log in</h5>', index_resp)

    def test_registration_page(self):
        self.assertIn(
            '<form action="/registration/" method="POST">',
            str(self.client.get('/registration/').content),
            )

    def test_wall_of_user_if_you_without_auth(self):
        resp = str(
            self.client.get('/wall/967103409/').content, encoding='utf-8',
            )
        self.assertIn('Максим Шаврин', resp)
        self.assertIn('Log in, please to see account info\n', resp)
        self.assertIn('unknown-user.jpg', resp)
        self.assertNotIn('Lorem', resp)

    def test_register(self):
        resp = str(
            self.client.post(
                '/registration/',
                data=dict(
                    email='test_user@test.com',
                    first_name='Test',
                    last_name='User',
                    password1='kufkutfy764754dsdddddh',
                    password2='kufkutfy764754dsdddddh',
                ),
                follow=True,
            ).content,
            encoding='utf-8',
            )
        self.assertIn('Tezt User', resp)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
