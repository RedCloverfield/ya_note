from http import HTTPStatus

from django.urls import reverse

from .custom_test_case import CustomTestCase


class TestRoutes(CustomTestCase):

    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_pages_availability_for_anonymous_user(self):
        """Тестирует доступность страниц проекта анонимному пользователю."""
        urls = (
            'notes:home',
            'users:signup',
            'users:login',
            'users:logout'
        )
        for page in urls:
            with self.subTest(page=page):
                url = reverse(page)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        """
        Тестирует доступность страниц проекта
        аутентифицированному пользователю.
        """
        urls = (
            'notes:list',
            'notes:success',
            'notes:add'
        )
        for page in urls:
            self.client.force_login(self.author)
            with self.subTest(page=page):
                url = reverse(page)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        """
        Тестирует доступность страниц просмотра,
        редактирования и удаления записи авторизированному
        и анонимному пользователям.
        """
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND)
        )
        urls = (
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,))
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for page, args in urls:
                with self.subTest(page=page, args=args):
                    url = reverse(page, args=args)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_user(self):
        """
        Тестирует перенаправления анонимного
        пользователя на страницу логина.
        """
        login_url = reverse('users:login')
        urls = (
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        for page, args in urls:
            with self.subTest(page=page, args=args):
                url = reverse(page, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
