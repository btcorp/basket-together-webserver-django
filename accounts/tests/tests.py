from django.test import TestCase
from django.http import HttpRequest
from .views import signup
from django.contrib.auth import get_user_model


class AccountsPageTest(TestCase):
    username_ = 'test00'
    password_ = '1234qwer'

    def test_signup_can_save_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = self.username_
        request.POST['password1'] = self.password_
        request.POST['password2'] = self.password_

        response = signup(request)

        print(response.content.decode())
        # self.assertIn(self.username_, response.content.decode())
        # self.assertIn(self.password_, response.content.decode())

    def test_saving_and_retrieving_users(self):
        user = get_user_model()
        first_user = user()
        first_user.username = 'test1'
        first_user.set_password('1234qwer')
        first_user.save()


        user = get_user_model()
        second_user = user()
        second_user.username = 'test2'
        second_user.set_password('1234qwer')
        second_user.save()

        saved_users = get_user_model().objects.all()
        self.assertEqual(saved_users.count(), 2)

        first_saved_user = saved_users[0]
        second_saved_user = saved_users[1]
        self.assertEqual(first_saved_user.username, first_user.username)
        self.assertEqual(second_saved_user.username, second_user.username)
