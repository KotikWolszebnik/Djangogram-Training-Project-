from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
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

    def register_user(self):
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
            .split('<a href="https://djgramm.herokuapp.com/confirm/')[1]\
            .split('/', maxsplit=1)[0]
        return resp

    def register_and_confirm(self):
        self.register_user()
        return self.client.get(f'/confirm/{self.unique_token}/')

    def register_confirm_and_post(self):
        resp = self.register_and_confirm()
        self.post_text = 'Post № 1: Creating test database for alias default...'
        Post.objects.create(
            id=1234567890,
            text=self.post_text,
            author=resp.wsgi_request.user)
        return self.client.get(f'/wall/{resp.wsgi_request.user.pk}/')

    def test_index_login_page(self):
        index_resp = str(self.client.get('/').content)
        self.assertIn('<h5 class="card-title">Log in</h5>', index_resp)

    def test_registration_page(self):
        self.assertIn(
            '<form action="/registration/" method="POST">',
            str(self.client.get('/registration/').content),
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
        resp = self.register_user()
        self.assertTrue(resp.wsgi_request.user.is_authenticated)
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('Test User', resp_str)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

    def test_login(self):
        self.register_user()
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
        self.register_user()
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
        resp = self.register_user()
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
        self.assertNotIn('unknown-user.jpg', resp_str)
        self.assertIn('lorem ipsum dolor', resp_str)

    def test_about_yourself(self):
        self.register_and_confirm()
        about_yourself = 'Creating test database for alias default...'
        resp = self.client.post(
            '/profile/',
            data=dict(about_yourself=about_yourself),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(about_yourself, resp_str)

    def test_post(self):
        self.register_and_confirm()
        post_text = 'Post № 1: Creating test database for alias default...'
        resp = self.client.post(
            '/post/',
            data=dict(text=post_text),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(post_text, resp_str)

    def test_wall_post_and_about_editing_regims(self):
        resp = self.register_confirm_and_post()
        resp_str = str(resp.content, encoding='utf-8')
        about_text = '<textarea required name="about_yourself" cols="35" rows="10" placeholder="About yourself:"></textarea>\n'
        self.assertNotIn(about_text, resp_str)
        resp = self.client.post(
            f'/wall/{resp.wsgi_request.user.pk}/',
            data=dict(edit_profile=True),
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(about_text, resp_str)
        resp = self.client.post(
            f'/wall/{resp.wsgi_request.user.pk}/',
            data=dict(edit_post_id=1234567890),
        )
        resp_str = str(resp.content, encoding='utf-8')
        edit_post_text = '<textarea name="text" cols="81" rows="5" placeholder="text">'
        self.assertIn(edit_post_text, resp_str)

    def test_edit_post(self):
        resp = self.register_confirm_and_post()
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(self.post_text, resp_str)
        changed_post_text = 'ChangedPost № 1: Creating test database for alias default...'
        resp = self.client.post(
            '/post/edit/',
            data=dict(
                post_id=1234567890,
                text=changed_post_text,
            ),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(changed_post_text, resp_str)
        self.assertIn('edited', resp_str)

    def test_delete_post(self):
        resp = self.register_confirm_and_post()
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn(self.post_text, resp_str)
        resp = self.client.post(
            '/post/delete/',
            data=dict(id=1234567890),
            follow=True,
        )
        resp_str = str(resp.content, encoding='utf-8')
        self.assertNotIn(self.post_text, resp_str)

    def test_delete_avatar(self):
        resp = self.register_and_confirm()
        resp_str = str(resp.content, encoding='utf-8')
        self.assertNotIn('unknown-user.jpg', resp_str)
        resp = self.client.post('/avatar/delete/', follow=True)
        resp_str = str(resp.content, encoding='utf-8')
        self.assertIn('unknown-user.jpg', resp_str)

    def test_logout(self):
        self.register_and_confirm()
        resp = self.client.post('/logout/', follow=True)
        self.assertFalse(resp.wsgi_request.user.is_authenticated)
