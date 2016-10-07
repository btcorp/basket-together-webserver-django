from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class SignupLoginTest(unittest.TestCase):
    username = 'test1'
    password1_ = '1234qwer'
    password2_ = '1234qwer'

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    # sign up, login test
    def test_signup_and_login(self):
        self.browser.get('http://localhost:8000/accounts/signup/')

        inputbox_username = self.browser.find_element_by_id('id_username')
        inputbox_pw1 = self.browser.find_element_by_id('id_password1')
        inputbox_pw2 = self.browser.find_element_by_id('id_password2')
        self.assertEqual(inputbox_username.get_attribute('placeholder'), 'Username or Email')

        inputbox_username.send_keys(self.username)
        inputbox_pw1.send_keys(self.password1_)
        inputbox_pw2.send_keys(self.password2_)
        inputbox_pw2.send_keys(Keys.ENTER)

        self.assertNotIn('/accounts/signup/', self.browser.current_url)
        self.assertIn('/accounts/login/', self.browser.current_url)

        inputbox_username = self.browser.find_element_by_id('id_username')
        inputbox_pw = self.browser.find_element_by_id('id_password')

        inputbox_username.send_keys(self.username)
        inputbox_pw.send_keys(self.password1_)
        inputbox_pw.send_keys(Keys.ENTER)

        self.assertNotIn('/accounts/login', self.browser.current_url)


if __name__ == '__main__':
    unittest.main()
