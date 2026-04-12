from django.test import TestCase, Client


class StatusPagesTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status(self):
        response = self.client.get('/results_all/', secure=True)
        self.assertEqual(response.status_code, 200)  # Проверка, что страница доступна (OK)
       
        

    