from django.test import TestCase, Client
import datetime as dt
#Авторизованный пользователь может опубликовать пост (new)
#Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
#После публикации поста новая запись появляется на главной странице сайта (index), на персональной странице пользователя (profile), и на отдельной странице поста (post)
#Авторизованный пользователь может отредактировать свой пост и его содержимое изменится на всех связанных страницах
class ProfileTest(TestCase):
        def setUp(self):
                self.client = Client()
                self.user = User.objects.create_user(
                        username="sarah", email="connor.s@skynet.com", password="12345"
                )
                self.post = Post.objects.create(text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!", author=self.user)
#После регистрации пользователя создается его персональная страница (profile)
        def test_profile(self):
                response = self.client.get("/sarah/")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.context["posts"]), 1)
                self.assertIsInstance(response.context["profile"], User)
                self.assertEqual(response.context["profile"].username, self.user.username)