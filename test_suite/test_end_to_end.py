import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from utils.steps import StartEnd, Converter


@pytest.allure.feature('End-to-end сценарий')
@pytest.allure.story('Ввод суммы, выбор некоторых опций, конвертация валюты')
class TestEndToEnd(StartEnd):

    def test_end_to_end(self):
        converter = Converter(self.driver)

        with pytest.allure.step('Ввод суммы'):
            # кликаем поле для ввода суммы
            converting_summ = converter.find(converter.summ)
            converting_summ.click()
            assert 'Не удалось найти и кликнуть в поле ввода суммы'

            # очищаем поле для ввода суммы
            converting_summ.clear()

            assert 'Не удалось очистить поле ввода суммы'

            # вводим сумму
            converting_summ.send_keys('1')
            assert 'Не удалось ввести сумму'

        with pytest.allure.step('Выбор опций'):
            # выбираем валюту, из которой конвертируем
            converterFrom = converter.find(converter.convFrom)
            converterFrom.click()
            assert 'Список валют "из" не открывается'

            # выбираем EUR
            eur = converter.find("//select[@name='converterFrom']/../div/div/span[text()='EUR']")
            eur.click()
            assert 'Не удалось выбрать валюту (EUR)'

            # выбираем валюту, в которую конвертируем
            converterTo = converter.find(converter.convTo)
            converterTo.click()
            assert 'Список валют "в" не открывается'

            # выбираем GBP
            gbp = converter.find("//select[@name='converterTo']/../div/div/span[text()='GBP']")
            gbp.click()
            assert 'Не удалось выбрать валюту (GBP)'

            # в блоке "Источник" выбираем "Наличные"
            source = converter.find(converter.cash)
            source.click()
            assert 'Не удалось выбрать "Источник" - "Наличные"'

            # в блоке "Получение" выбираем "Выбрать наличные"
            destination = converter.find(converter.choose_cash)
            destination.click()
            assert 'Не удалось выбрать "Получение" - "Выбрать наличные"'

        with pytest.allure.step('Вывод результата с помощью кнопки "Показать"'):
            # нажимаем "Показать"
            button = converter.find(converter.show_button)
            button.click()

            # ждем, когда появится блок с результатом
            try:
                WebDriverWait(self.driver, 10).until(
                    ec.text_to_be_present_in_element((By.XPATH, converter.result_to), '0,82'))
            except TimeoutException:
                raise Exception('Значение не получено')

            converterFrom_sel = converter.get_text(converter.convFrom_select)
            converterTo_sel = converter.get_text(converter.convTo_select)

            with pytest.allure.step('Проверка результата'):
                assert converterFrom_sel == 'EUR', 'Неверная валюта "из"'
                assert converterTo_sel == 'GBP', 'Неверная валюта "в"'
