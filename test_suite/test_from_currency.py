import pytest
from utils.steps import StartEnd, Converter
from data.testing_data import get_currencies_data

params_list = get_currencies_data()


@pytest.fixture(scope="function", params=params_list)
def param_test(request):
    return request.param


class TestFromCurrency(StartEnd):
    @pytest.allure.feature('CRUD-тест: выбор валюты')
    @pytest.allure.story('Выбор валюты, из которой конвертируем, проверка списка')
    def test_from_currency(self, param_test):
        input, expected_output = param_test
        result = Converter(self.driver).from_currency_func(input)
        with pytest.allure.step('Проверка результата'):
            assert result == input, 'Не удалось выбрать нужную валюту'
