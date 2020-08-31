from django.test import Client, TestCase

from .models import Post, Group


class ProfileTest(TestCase):

    url1 = reverse('post', kwargs=username)
    url2 = reverse('post_edit', kwargs=username)

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="sarah",
                                     email="connor.s@skynet.com",
                                     password="Password123$")
        self.client.force_login(self.user)
        print("Создали тестового пользователя")
        self.group = Group.objects.create(title='Test group',
                                          slug='testgroup',
                                          description='Test Group')
        print("Создали тестовую группу")
        self.post = Post.objects.create(
            text="Hello world",
            author=self.user
        )
        print("Создали тестового поста авторизованным пользователем")
        self.assertRedirects(response,
                             reverse('profile', kwargs=username),
                             status_code=200
        )
        print("Создана персональная страница (profile)")
        self.assertEqual(response.status_code, 200)
        print("проверяем что страница найдена")

    def testPublicPost(self):
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code=200)
        self.assertIn(self.post, response.context['page'].object_list)
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code = 200)
        self.assertIn(self.post, response.context['page'].object_list)
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code = 200)
        self.assertIn(self.post, response.context['page']
        response = self.client.get("/")
        print("новая запись появляется на (index), (profile), (post)")

    def testPostEdit(self):
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200,
                         msg='Проблемы на странице поста для редактирования.',
        data = {'text': 'terminator', 'id': 2000, 'group': group}
        )
        response = self.client.post(self.url2, data)
        response = self.client.get('/')
        self.assertContains(response, 'terminator222',
                            msg_prefix='Проблема после редактирования текста'
        )
        response = self.client.get(self.url2)
        self.assertContains(response, 'termo',
                            msg_prefix='Проблема после редактирования группы'
        )

    def testGuest(self):
        #Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа
        self.client.force_login(self.user)
        response = self.client.post(reverse('post_new'), follow=True)
        self.assertRedirects(
            response,
            reverse('index'),
            status_code=301
        )