import pytest
from data.testing_data import get_converter_data
from utils.steps import StartEnd, Converter

params_list = get_converter_data()


@pytest.fixture(scope="function", params=params_list)
def param_test(request):
    return request.param


@pytest.allure.feature('Калькулятор иностранных валют. CRUD-тест: поле ввода суммы')
@pytest.allure.story('Ввод различных параметров и проверка результата')
class TestConverter(StartEnd):
    def test_converter(self, param_test):
        input, expected_output = param_test
        result = Converter(self.driver).converter_func(input, expected_output)
        with pytest.allure.step('Проверка результата'):
            assert result == expected_output, 'Результат не совпадает с ожидаемым'
