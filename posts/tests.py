from django.test import TestCase, Client
from posts.models import Post, Group

class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="sarah",
                                     email="connor.s@skynet.com",
                                     password="Password123$")
        self.client.force_login(self.user)
        print("Создали тестового пользователя")
        self.group = Group.objects.create(title='Test group', slug='testgroup', description='Test Group')
        print("Создали тестовую группу")
        self.post = Post.objects.create(
            text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.user
        )
        print("Создали тестовый пост")

    def test_profile(self):
        response = self.client.post('/auth/singup/',
                                    self.user, follow=true
                                    )
        self.assertRedirects(response, '/auth/login/', status_code=200)
        print("После регистрации пользователя создается его персональная страница (profile)")
        self.assertEqual(response.status_code, 200)
        print("проверяем что страница найдена")

    def new_post(self):
        response = self.client.get('/?page=1/')
        self.assertEqual(response.status_code=200)
        self.assertIn(self.post, response.context['page'].object_list)
        response = self.client.get(f'/{self.user.username}/?page=1/')
        self.assertEqual(response.status_code = 200)
        self.assertIn(self.post, response.context['page'].object_list)
        response = self.client.get(f'/{self.user.username}/{self.post.id}/')
        self.assertEqual(response.status_code = 200)
        self.assertIn(self.post, response.context['page']
        print("Авторизованный пользователь может опубликовать пост")

        response = self.client.get("/")
        print("После публикации поста новая запись появляется на главной странице сайта (index), на персональной странице пользователя (profile), и на отдельной странице поста (post)")

    def post_edit(self):
        response = self.client.get('/sarah/2000/edit/')
        self.assertEqual(response.status_code, 200,
                         msg='Проблемы на странице поста для редактирования.')
        data = {'text': 'terminator', 'id': 2000, 'group': group}
        response = self.client.post('/sarah/2000/edit/', data)
        response = self.client.get('/')
        self.assertContains(response, 'terminator222', msg_prefix='Проблема после редактирования: не сохранился результат редактирования текста')
        response = self.client.get('/sarah/2000/edit/')
        self.assertContains(response, 'termo', msg_prefix='Проблема после редактирования: не сохранился результат редактирования группы')

class guest_test(TestCase):
    def test_guest(self):
        #Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа
        self.client.force_login(self.user)
        response = self.client.post(
            '/new', {'text': 'Test post', 'group': self.group.id}, follow=True
        )
        self.assertRedirects(
            response,
            reverse('index'),
            status_code=301
        )