from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course,Note


class UserTest(TestCase):
     
    def test_create_user(self):
        user = User.objects.create_user(
                username="old user",
                password="123456"
          )
        self.assertEqual(user.username,"old user")


    def test_login(self):
        User.objects.create_user(
                username="old user",
                password="123456"
        )

        login =self.client.login(
                username="old user",
                password="123456"
        )
        
        self.assertTrue(login)

    def test_course_belongs_to_user(self):
        user = User.objects.create_user(
                username="old user",
                password="123456"
        )

        course =Course.objects.create(
            title="Python",
            user=user
        )

        self.assertEqual(course.user,user)

    def test_user_only_see_his_courses(self):
        user1=User.objects.create(
            username="new user",
            password="654321"
        )

        user2=User.objects.create(
            username="old user",
            password="123456"
        )

        Course.objects.create(
            title="Math",
            user=user1
        )

        Course.objects.create(
            title="Python",
            user=user2
        )

        self.assertTrue(Course.objects.filter(user=user1,title="Math").exists())


class courseModelTest(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(
                username="old user",
                password="123456"
          )
    def test_create_course(self):
        course=Course.objects.create(
            title="Python",
            description="python course",
            user=self.user
        )

        self.assertEqual(course.title,"Python")
        self.assertEqual(course.description,"python course")
        self.assertEqual(course.user,self.user)


class NoteModelTest(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(
                username="old user",
                password="123456"
          )

        self.course=Course.objects.create(
            title="Python",
            description="python course",
            user=self.user
        )
    def test_create_note(self):

        note = Note.objects.create(
            title="note_management",
            content="This project helps us manage our course notes",
            course=self.course
        )

        self.assertEqual(note.title,"note_management")
        self.assertEqual(note.content,"This project helps us manage our course notes")
        self.assertEqual(note.course,self.course)


class NoteSearchTest(TestCase):

    def setUp(self):
        self.user=User.objects.create_user(
            username="old user",
            password="123456"
        )

        self.course=Course.objects.create(
            title="Python",
            description="python course",
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