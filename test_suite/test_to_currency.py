import pytest
from utils.steps import StartEnd, Converter
from data.testing_data import get_currencies_data

params_list = get_currencies_data()


@pytest.fixture(scope="function", params=params_list)
def param_test(request):
    return request.param


class TestCurrency(StartEnd):
    @pytest.allure.feature('CRUD-тест: выбор валюты')
    @pytest.allure.story('Выбор валюты, в которую конвертируем, проверка списка')
    def test_to_currency(self, param_test):
        input, expected_output = param_test
        result = Converter(self.driver).to_currency_func(input)
        with pytest.allure.step('Проверка результата'):
            assert result == input, 'Не удалось выбрать нужную валюту'
