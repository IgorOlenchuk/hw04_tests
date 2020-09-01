from audioop import reverse

from django.test import Client, TestCase

from .models import Post, Group

from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.guest = Client()
        self.user = User.objects.create_user(username="sarah",
                                     email="connor.s@skynet.com",
                                     password="Password123$")
        self.client.force_login(self.user)
        self.group = Group.objects.create(title='Test group',
                                          slug='testgroup',
                                          description='Test Group')
        self.post = Post.objects.create(
            text="Hello world",
            author=self.user
        )
#        self.url1 = reverse('post', {"username": self.user, "post_id": 1})
#        self.url2 = reverse('post_edit', {"author": self.user})

    def test_user_page_created(self):
        response = self.client.get('<str:username>/',
                                           {"author": self.user})
        self.assertEqual(response.status_code, 200,
                         msg="Страницы пользователя не существует")
        self.assertRedirects('<str:username>/', {"username": self.user},
                             status_code=200
        )

    def test_public_post(self):
        test_context = {
            "author": self.user,
            "group": self.group,
            "text": "This is my first post!",
        }
        response = self.client.post("new/", test_context, follow=True)
        self.assertEqual(response.status_code, 200,
                         msg="Пост не создан")
        response = self.client.get('<str:username>/<int:post_id>/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post, response.context['page'].object_list)
        response = self.client.get('<str:username>/<int:post_id>/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post, response.context['page'].object_list)
        response = self.client.get('<str:username>/<int:post_id>/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post, response.context['page'])
        response = self.client.get(reverse('index'))
        print("новая запись появляется на (index), (profile), (post)")

    def test_post_edit(self):
        test_context={'text': 'terminator', 'id': 2000, 'group': self.group}
        response = self.client.get('<str:username>/<int:post_id>/edit/', test_context)
        self.assertEqual(response.status_code, 200, msg='Проблемы на странице поста для редактирования.')
        response = self.client.post('<str:username>/<int:post_id>/edit/', test_context)
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'terminator222',
                            msg_prefix='Проблема после редактирования текста'
        )
        response = self.client.get('<str:username>/<int:post_id>/edit/')
        self.assertContains(response, 'termo',
                            msg_prefix='Проблема после редактирования группы'
        )

    def test_guest(self):
        redirect_url = '/auth/login/?next=/new/'
        response = self.guest.get("new/")
        self.assertEqual(response.status_code, 302,
                         msg="Страница новой записи доступна "
                             "guest или переадрессация не произошла")
        self.assertRedirects(response, redirect_url, status_code=302,
                             msg_prefix='Неверный редирект')

    def test_debug(self):
        self.guest = Client()
        test_context={'text': 'terminator', 'id': 2000, 'group': self.group}
        response = self.guest.get('new/', test_context)
        self.assertEqual(response.status_code, 200, msg='Проблемы на странице поста для редактирования.')
        response = self.guest.post(reverse('new_post'), data)
        response = self.guest.get(reverse('index'))
        self.assertContains(response, 'terminator222',
                            msg_prefix='Проблема после редактирования текста'
        )
        response = self.client.get('<str:username>/<int:post_id>/edit/')
        self.assertContains(response, 'termo',
                            msg_prefix='Проблема после редактирования группы'
        )

    def test_image(self):
        self.guest = Client()
        response = self.guest.post("")
        self.assertEqual(response.status_code, 200, msg='Проблемы на странице поста для редактирования.')
        response = self.guest.post('<str:username>/', {'username': 'leo'})
        self.assertContains(response, 'leo', msg_prefix='Проблема после редактирования текста')
        response = self.guest.post("group/<slug:slug>", {'group': 'Cats'})
        self.assertContains(response, 'Cats', msg_prefix='Проблема после редактирования группы')