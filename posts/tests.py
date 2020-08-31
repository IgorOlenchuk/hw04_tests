from django.test import Client, TestCase

from .models import Post, Group


class ProfileTest(TestCase):

    def setUp(self):
        self.url1 = reverse('post', kwargs=username)
        self.url2 = reverse('post_edit', kwargs=username)
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

    def test_user_page_created(self):
        response = self.client.get(reverse("profile",
                                           kwargs={
                                                   "username": self.user}))
        self.assertEqual(response.status_code, 200,
                         msg="Страницы пользователя не существует")
        self.assertRedirects(response,
                             reverse('profile', kwargs=username),
                             status_code=200
        )

    def test_Public_Post(self):
        url = reverse("new_post")
        test_context = {
            "group": self.group.id,
            "text": "This is my first post!",
        }
        response = self.client.post(url, test_context, follow=True)
        self.assertEqual(response.status_code, 200,
                         msg="Пост не создан")
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code=200)
        self.assertIn(self.post, response.context['page'].object_list)
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code = 200)
        self.assertIn(self.post, response.context['page'].object_list)
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code = 200)
        self.assertIn(self.post, response.context['page'])
        response = self.client.get(reverse('index'))
        print("новая запись появляется на (index), (profile), (post)")

    def test_Post_Edit(self):
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200,
                         msg='Проблемы на странице поста для редактирования.',
        data = {'text': 'terminator', 'id': 2000, 'group': group}
        )
        response = self.client.post(self.url2, data)
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'terminator222',
                            msg_prefix='Проблема после редактирования текста'
        )
        response = self.client.get(self.url2)
        self.assertContains(response, 'termo',
                            msg_prefix='Проблема после редактирования группы'
        )

    def test_Guest(self):
        url = reverse('new_post')
        redirect_url = '/auth/login/?next=/new/'
        response = self.guest.get(url)
        self.assertEqual(response.status_code, 302,
                         msg="Страница новой записи доступна "
                             "guest или переадрессация не произошла")
        self.assertRedirects(response, redirect_url, status_code=302,
                             msg_prefix='Неверный редирект')