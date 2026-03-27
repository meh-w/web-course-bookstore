from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from users.models import User
from homepage.models import Book
from orders.models import Order
from cart.models import Cart, CartItem


class OrderTest(LiveServerTestCase):

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
            username="testuser", password="t21testpass7829"
        )

        self.book = Book.objects.create(
            title="Test Book", author="Author", price=100
        )

    def login(self):
        browser = self.browser
        browser.get(f"{self.live_server_url}/users/login/")

        browser.find_element(By.NAME, "username").send_keys("testuser")
        browser.find_element(By.NAME, "password").send_keys("t21testpass7829")
        browser.find_element(By.NAME, "password").submit()

        WebDriverWait(browser, 5).until(
            ec.url_to_be(f"{self.live_server_url}/")
        )

    def create_cart_with_item(self):
        cart = Cart.objects.create(user=self.user)

        CartItem.objects.create(cart=cart, book=self.book, quantity=2)

    def test_order_create_success(self):
        browser = self.browser

        self.login()
        self.create_cart_with_item()

        browser.get(f"{self.live_server_url}/cart/")

        order_button = WebDriverWait(browser, 5).until(
            ec.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
            )
        )

        order_button.click()

        WebDriverWait(browser, 5).until(ec.url_contains("/orders/"))

        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()
        self.assertEqual(order.items.count(), 1)

        body = browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Заказ #", body)
        self.assertIn("Test Book", body)
        self.assertIn("200", body)

    def test_order_empty_cart(self):
        browser = self.browser

        self.login()

        Cart.objects.create(user=self.user)

        browser.get(f"{self.live_server_url}/cart/")

        body = browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Ваша корзина пуста", body)

    def test_cart_cleared_after_order(self):
        browser = self.browser

        self.login()
        self.create_cart_with_item()

        browser.get(f"{self.live_server_url}/cart/")

        order_button = WebDriverWait(browser, 5).until(
            ec.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
            )
        )

        order_button.click()

        WebDriverWait(browser, 5).until(ec.url_contains("/orders/"))

        browser.get(f"{self.live_server_url}/cart/")

        body = browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Ваша корзина пуста", body)
