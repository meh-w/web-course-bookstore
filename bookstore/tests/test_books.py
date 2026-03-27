from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from users.models import User
from homepage.models import Book


class BookCrudTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        service = Service(ChromeDriverManager().install())
        cls.browser = webdriver.Chrome(service=service)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.admin = User.objects.create_user(
            username="adminuser", password="testpass123", role="admin"
        )

    def login_admin(self):
        browser = self.browser
        browser.get(f"{self.live_server_url}/users/login/")
        browser.find_element(By.NAME, "username").send_keys("adminuser")
        browser.find_element(By.NAME, "password").send_keys("testpass123")
        browser.find_element(By.NAME, "password").submit()
        WebDriverWait(browser, 5).until(
            ec.url_to_be(f"{self.live_server_url}/")
        )

    def test_add_edit_delete_book(self):
        browser = self.browser
        self.login_admin()

        browser.get(f"{self.live_server_url}/book/add/")
        WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.NAME, "title"))
        )

        browser.find_element(By.NAME, "title").send_keys("Test Book")
        browser.find_element(By.NAME, "author").send_keys("Test Author")
        browser.find_element(By.NAME, "price").send_keys("250")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(browser, 5).until(
            ec.url_to_be(f"{self.live_server_url}/")
        )
        book = Book.objects.get(title="Test Book")
        self.assertEqual(book.price, 250)

        browser.get(f"{self.live_server_url}/book/{book.id}/edit/")
        WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.NAME, "price"))
        )

        price_input = browser.find_element(By.NAME, "price")
        price_input.clear()
        price_input.send_keys("300")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(browser, 5).until(
            ec.url_to_be(f"{self.live_server_url}/")
        )
        book.refresh_from_db()
        self.assertEqual(book.price, 300)

        browser.get(f"{self.live_server_url}/")
        WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.CLASS_NAME, "card"))
        )

        cards = browser.find_elements(By.CLASS_NAME, "card")
        for card in cards:
            if "Test Book" in card.text:
                delete_btn = card.find_element(
                    By.XPATH, ".//button[contains(text(), 'Удалить')]"
                )
                delete_btn.click()
                break

        WebDriverWait(browser, 2).until(ec.alert_is_present())
        browser.switch_to.alert.accept()

        WebDriverWait(browser, 5).until(
            ec.url_to_be(f"{self.live_server_url}/")
        )

        self.assertFalse(Book.objects.filter(id=book.id).exists())
