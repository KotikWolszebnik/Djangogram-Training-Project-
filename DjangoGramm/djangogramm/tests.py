from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.lorem_ipsum import words

from .models import Account, Picture, Post


# Create your tests here.
class YourTestClass(TestCase):

    def setUp(self):
        self.account = Account.objects.create(
            slug=967103409,
            email='test@user.com',
            password='password',
            first_name='Максим',
            last_name='Шаврин',
            bio=words(16),
        )
        for item in range(7):
            Post(text=words(16), author=self.account).save()

    def register_user(self):
        """Make the fixture."""
        resp = self.client.post(
            '/registration/',
            data=dict(
                email='test_user@test.com',
                first_name='Test',
                last_name='User',
                password1='kufkutfy764754dsdddddh',
                password2='kufkutfy764754dsdddddh',
            ),
            follow=True,
        )
        self.unique_token = str(mail.outbox[0].message())\
            .split('/confirm/')[1].split('/', maxsplit=1)[0]
        return resp

    def register_and_confirm(self):
        """Make the fixture."""
        self.register_user()
        return self.client.get(f'/confirm/{self.unique_token}/')

    def register_confirm_and_post(self):
        """Make the fixture."""
        resp = self.register_and_confirm()
        self.post_text = 'Присваивание в условии цикла - Python - Киберфорум'
        Post.objects.create(
            slug=1234567890,
            text=self.post_text,
            author=resp.wsgi_request.user)
        return self.client.get(f'/wall/{resp.wsgi_request.user.slug}/')

    def test_index_login_page(self):
        index_resp = str(self.client.get('/').content, encoding='utf-8')
        self.assertIn('<h5 class="card-title">Log in</h5>', index_resp)

    def test_registration_page(self):
        resp = self.client.get('/registration/')
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(
            '<form action="/registration/" method="POST">', resp_str,
            )

    def test_wall_of_user_if_you_without_auth(self):
        resp = self.client.get('/wall/967103409/')
        self.assertFalse(resp.wsgi_request.user.is_authenticated)
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('Максим Шаврин', resp_str)
        self.assertIn('Log in, please to see account info\n', resp_str)
        self.assertIn('unknown-user.jpg', resp_str)
        self.assertNotIn('Lorem', resp_str)

    def test_register(self):
        resp = self.register_user()  # fixture

        self.assertTrue(resp.wsgi_request.user.is_authenticated)
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('Test User', resp_str)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

    def test_login(self):
        self.register_user()  # fixture

        resp = self.client.post(
            '/login/',
            data=dict(
                username='test_user@test.com',
                password='kufkutfy764754dsdddddh',
            ),
            follow=True,
        )
        self.assertTrue(resp.wsgi_request.user.is_authenticated)
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('Test User', resp_str)

    def test_wall_of_user_if_you_without_confirm(self):
        self.register_user()  # fixture

        resp = self.client.get('/wall/967103409/')
        resp_str = str(resp.content, encoding='utf-8')
        self.assertTrue(resp.wsgi_request.user.is_authenticated)
        self.assertIsNone(resp.wsgi_request.user.reg_confirmed_date)
        self.assertIn('Максим Шаврин', resp_str)
        self.assertIn(
            'You can\'t see another user info, posts and pictures before conf',
            resp_str,
        )
        self.assertIn('unknown-user.jpg', resp_str)
        self.assertNotIn('Lorem', resp_str)

    def test_confirm(self):
        resp = self.register_user()  # fixture

        self.assertIsNone(resp.wsgi_request.user.reg_confirmed_date)

        self.client.get(f'/confirm/{self.unique_token}/')
        resp = self.client.get('/wall/967103409/')
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIsNotNone(resp.wsgi_request.user.reg_confirmed_date)
        self.assertIn('Максим Шаврин', resp_str)
        self.assertNotIn(
            'You can\'t see another user info, posts and pictures before conf',
            resp_str,
        )
        self.assertIn('lorem ipsum dolor', resp_str)

    def test_about_yourself(self):
        self.register_and_confirm()  # fixture

        bio = 'Creating test database for alias default...'
        resp = self.client.post(
            '/bio/edit/',
            data=dict(bio=bio),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(bio, resp_str)

    def test_post(self):
        self.register_and_confirm()  # fixture

        post_text = 'Post № 1: Creating test database for alias default...'
        resp = self.client.post(
            '/post/create/',
            data=dict(text=post_text),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(post_text, resp_str)

    def test_wall_post_and_about_editing_regims(self):
        resp = self.register_confirm_and_post()  # fixture

        resp_str = str(resp.content, encoding='utf-8')
        about_text = '<textarea name="bio" cols="40" rows="10" maxlength="150" id="id_bio">\n</textarea></p>'
        self.assertNotIn(about_text, resp_str)

        resp = self.client.post(
            f'/wall/{resp.wsgi_request.user.slug}/',
            data=dict(edit_profile=True),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(about_text, resp_str)

        resp = self.client.post(
            f'/wall/{resp.wsgi_request.user.slug}/',
            data=dict(edit_post_slug=1234567890),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        edit_post_text = '<textarea name="text" cols="40" rows="10" maxlength="2200" id="id_text">\n</textarea>'
        self.assertIn(edit_post_text, resp_str)

    def test_edit_post(self):
        resp = self.register_confirm_and_post()  # fixture

        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(self.post_text, resp_str)
        changed_post_text = 'ChangedPost № 1: Creating test database for alias default...'
        
        resp = self.client.post(
            '/post/edit/',
            data=dict(
                post_slug=1234567890,
                text=changed_post_text,
            ),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(changed_post_text, resp_str)
        self.assertIn('edited', resp_str)

    def test_delete_post(self):
        resp = self.register_confirm_and_post()  # fixture

        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(self.post_text, resp_str)
        resp = self.client.post(
            '/post/delete/',
            data=dict(slug=1234567890),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertNotIn(self.post_text, resp_str)

    def test_logout(self):
        self.register_and_confirm()  # fixture

        resp = self.client.post('/logout/', follow=True)
        self.assertFalse(resp.wsgi_request.user.is_authenticated)
