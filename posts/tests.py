from django.test import TestCase, Client
import datetime as dt

class TestStringMethods(TestCase):
    def test_length(self):
                self.assertEqual(len('yatube'), 6)

    def test_show_msg(self):
                # действительно ли первый аргумент — True?
                self.assertTrue(False, msg="Важная проверка на истинность")





# Create your tests here.

# Задание

# Напишите тесты для проверки страницы сайта с тарифными планами.

# Проверьте, что:
# - главная страница доступна неавторизованному пользователю, а раздел администратора — нет
# - переменная plans есть в контексте шаблона
# - имя шаблона, который вызывается при рендеринге главной страницы — index.html
# - тип переменной plans — это список, состоящий из 3-х элементов, а их тип — словарь
# - на результирующей странице показываются названия тарифных планов и подставляется правильная тема (subject) в ссылку на кнопке "Связаться"
# - в контекстных переменных шаблона присутствует текущий год и он же правильно появляется на странице


class PlansPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def testPageCodes(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("admin/")
        self.assertEqual(response.status_code, 404)

    def testIndexContext(self):
        response = self.client.get("")
        self.assertIn('year', response.context)

        # переменная plans есть в контексте шаблона

    def testIndexTemplate(self):
        response = self.client.get("")
        #self.assertEqual(response.templates, index.html)
        self. assertTemplateUsed(response=None, template_name="index.html", msg_prefix='', count=None)
        # имя шаблона, который вызывается при рендеринге главной страницы — index.html

    def testIndexPlans(self):
        self.assertEqual(len(response.context['plans']), 3)
        self.assertIsInstance(type(response.context['plans']), dict)
        # тип переменной plans — это список, состоящий из 3-х элементов, а их тип — словарь

    def testIndexContent(self):
        # на результирующей странице показываются названия тарифных планов и подставляется правильная тема (subject) в ссылку на кнопке "Связаться"
        # Проверяйте вхождение строки f"mailto:order@company.site?subject={plan['name']}"
        response = self.client.get("")
        text = "Dogs"
        self.assertContains(response, text, count=None, status_code=200, msg_prefix='', html=False)


    def testContextProcessor(self):
        # в контекстных переменных шаблона присутствует текущий год и он же правильно появляется на странице
        # today = dt.datetime.today().year
        response = self.client.get("")
        self.assertEqual(response.context['today'], dt.datetime.today().year)