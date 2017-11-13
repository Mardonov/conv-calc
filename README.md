Автоматизация тестирования Калькулятора иностранных валют

Для запуска автотестов:
1) Активируйте virtualenv.
2) py.test --alluredir \[path_to_report_dir\]
3) allure generate directory-with-results/

Окружение проекта:

python 3.6

chromedriver-installer==0.0.6

pytest==2.9.0

pytest-allure-adaptor==1.7.9

selenium==3.7.0
