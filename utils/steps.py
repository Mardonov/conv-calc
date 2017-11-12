from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import pytest
import allure
from selenium.common.exceptions import NoSuchElementException


class StartEnd:
    # открыть браузер, загрузить страницу
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
        self.driver.get('http://www.sberbank.ru/ru/quotes/converter')
        with pytest.allure.step('Загрузка страницы'):
            assert 'Калькулятор иностранных валют' in self.driver.title, 'Страница не загрузилась'

    # закрыть браузер
    def teardown_class(self):
        self.driver.quit()


class Driver:
    def __init__(self, driver):
        self.driver = driver


class Converter(Driver):
    summ = "//input[@placeholder='Сумма']"
    convFrom = "//select[@name='converterFrom']/.."
    convTo = "//select[@name='converterTo']/.."
    cash = "//div[contains(concat(@class,' '),'kit-radio__text') and text()='Наличные']"
    choose_cash = "//div[contains(concat(@class,' '),'kit-radio__text') and text()='Выдать наличные']"
    show_button = "//button[@class='rates-button' and text()='Показать']"
    result_to = "//span[@class='rates-converter-result__total-to']"
    convFrom_select = "//select[@name='converterFrom']/..//strong"
    convTo_select = "//select[@name='converterTo']/..//strong"  # найти элемент по xpath

    def find(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return "Invalid xpath!"
        return self.driver.find_element_by_xpath(xpath)

    def get_text(self, xpath):
        return self.driver.find_element_by_xpath(xpath).text

    # ввод суммы и конвертация
    @pytest.fixture()
    def converter_func(self, input, output):

        with pytest.allure.step('Ввод новых данных в поле "Сумма"'):
            # находим и кликаем поле для ввода суммы
            summa = self.find(Converter.summ)
            summa.click()
            assert 'Не удалось выделить поле для ввода суммы'

            # очищаем поле для ввода суммы
            summa.clear()
            summa.clear()
            summa.clear()
        assert 'Не удалось очистить поле для ввода суммы'

        # вводим данные
        summa.send_keys(input)
        assert 'Не удалось ввести данные'

        with pytest.allure.step('Вывод результата'):
            # кликаем по кнопке "Показать"
            button = self.find(self.show_button)
            button.click()
        assert 'Не удалось нажать кнопку "Показать"'
        # ждем, когда значение в блоке с результатом обновится (совпадения знаков до запятой)
        try:
            WebDriverWait(self.driver, 10).until(ec.text_to_be_present_in_element((By.XPATH, self.result_to), output[:-3]))
            text = self.find(self.result_to).text[:-4]  # заменяем запятую на точку для сравнения результата
            text = text[:-3] + '.' + text[-2:]
            return text

        except TimeoutException:
            raise Exception('Значение не получено')

    # проверить список валют "из"
    def from_currency_func(self, data):
        xpath2 = "//select[@name='converterFrom']/..//span[contains(text()," + " '" + data + "'" + ")]"

        # находим и кликаем список валюты
        currency = self.find(self.convFrom)
        currency.click()

        with pytest.allure.step('Выбор валюты из списка'):
            # находим валюту в списке и выбираем ее
            currency_item = self.find(xpath2)
            currency_item.click()
            return currency.text

    # Проверить список валют "в"
    def to_currency_func(self, data):
        xpath2 = "//select[@name='converterTo']/..//span[contains(text()," + " '" + data + "'" + ")]"

        # находим и кликаем список валюты
        converterTo = self.find(self.convTo)
        converterTo.click()

        with pytest.allure.step('Выбор валюты из списка'):
            # находим валюту в списке и выбираем ее
            currency_item = self.find(xpath2)
            currency_item.click()
            return converterTo.text
