from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from users.models import User


class LoginTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="t21testpass7829", first_name="Test"
        )

    def test_login_success(self):
        browser = self.browser
        browser.get(f"{self.live_server_url}/users/login/")

        browser.find_element(By.NAME, "username").send_keys("testuser")
        browser.find_element(By.NAME, "password").send_keys("t21testpass7829")

        browser.find_element(By.NAME, "password").submit()

        WebDriverWait(browser, 5).until(
            ec.url_to_be(f"{self.live_server_url}/")
        )

        body = browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("С возвращением", body)

    def test_login_fail_wrong_credentials(self):
        browser = self.browser
        browser.get(f"{self.live_server_url}/users/login/")

        browser.find_element(By.NAME, "username").send_keys("wrong")
        browser.find_element(By.NAME, "password").send_keys("wrong")
        browser.find_element(By.NAME, "password").submit()

        WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        body = browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Неверный логин или пароль", body)

    def test_login_fail_wrong_password(self):
        browser = self.browser
        browser.get(f"{self.live_server_url}/users/login/")

        browser.find_element(By.NAME, "username").send_keys("testuser")
        browser.find_element(By.NAME, "password").send_keys("wrong")
        browser.find_element(By.NAME, "password").submit()

        WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        body = browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Неверный логин или пароль", body)
