from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course,Note


class NoteSearchTest(TestCase):

    def setUp(self):
        self.user=User.objects.create_user(
            username="old user",
            password="123456"
        )

        self.course=Course.objects.create(
            title="Python",
            user=self.user
        )

        Note.objects.create(
            title="note_management",
            content="This project helps us manage our course notes",
            course=self.course
        )

        Note.objects.create(
            title="Django",
            content="Django workes here!",
            course=self.course
        )

    def test_search_by_title(self):
            self.client.login(
                username="old user",
                password="123456"
            )

            response =self.client.get(
                "/notes/",
                {"q":"Django"}
            )

            self.assertContains(response,"Django")
            self.assertNotContains(response,"management")


    def test_search_by_content(self):
            self.client.login(
                username="old user",
                password="123456"
            )

            response =self.client.get(
                "/notes/",
                {"q":"course"}
            )

            self.assertContains(response,"course")
            self.assertNotContains(response,"work")