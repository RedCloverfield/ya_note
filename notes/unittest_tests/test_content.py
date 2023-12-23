from django.urls import reverse

from .custom_test_case import CustomTestCase


class TestContent(CustomTestCase):

    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_notes_list_for_different_users(self):
        """
        Проверяет, что записи одного пользователя не попадают
        на страницу записей другого пользователя.
        """
        note_in_list = (
            (self.author, True),
            (self.reader, False)
        )
        for user, note_status in note_in_list:
            self.client.force_login(user)
            with self.subTest(user=user, note_status=note_status):
                url = reverse('notes:list')
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertEqual((self.note in object_list), note_status)

    def test_pages_contains_form(self):
        """
        Проверяет наличие формы на страницах
        добавления и редактирования записи.
        """
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        self.client.force_login(self.author)
        for page, args in urls:
            url = reverse(page, args=args)
            responce = self.client.get(url)
            self.assertIn('form', responce.context)
