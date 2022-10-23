import pytest
import allure
from django.middleware.csrf import _get_new_csrf_string
from shop.models import Product, User, Order


@allure.feature('Страницы открываются')
@allure.story('Получение страницы')
@pytest.mark.parametrize("input_param, expected", [
    ("", 200),
    ("login", 200),
    ("register", 200),
    ("profile", 200),
    ("service", 200),
    ("service/1", 200),
    ("admin", 200)
])
def test_get_home(input_param, expected, test_main):
    response = test_main.get(input_param)

    with allure.step("Запрос отправлен, посмотрим код ответа"):
        assert response.status_code == expected, f"Неверный код ответа, получен {response.status_code}"


@allure.feature('Тесты пользователя')
@allure.story('Заказ продукта 1')
@pytest.mark.parametrize("input_param, expected", [
    ("service/1/order", 200)
])
def test_get_order(input_param, expected, test_main):
    token_sec = _get_new_csrf_string()
    response = test_main.get('login', headers={'Cookie': f'csrftoken={token_sec}'})
    index_start = response.text.find('csrfmiddlewaretoken')
    index_start = response.text.find('value', index_start)
    index_start = response.text.find('"', index_start) + 1
    index_end = response.text.find('"', index_start)
    csrfmiddlewaretoken = response.text[index_start:index_end]
    datas = {
        'username': "admin",
        'password': "admin",
        'csrfmiddlewaretoken': csrfmiddlewaretoken
    }
    response = test_main.post("login", data=datas,
                              headers={'Cookie': f'csrftoken={token_sec}',
                                       'Content-Type': 'application/x-www-form-urlencoded'})
    with allure.step("Запрос отправлен, посмотрим код ответа"):
        assert response.status_code == 200, f"Неверный код ответа, получен {response.status_code}"

    cookie = response.request.headers.get('Cookie')
    response = test_main.get(input_param, headers={'Cookie': cookie})

    with allure.step("Запрос отправлен, посмотрим код ответа"):
        assert response.status_code == expected, f"Неверный код ответа, получен {response.status_code}"


@allure.feature('Тесты пользователя')
@allure.story('На странице пользователя отображаются заказы')
def test_profile(test_main):
    token_sec = _get_new_csrf_string()
    response = test_main.get('login', headers={'Cookie': f'csrftoken={token_sec}'})
    index_start = response.text.find('csrfmiddlewaretoken')
    index_start = response.text.find('value', index_start)
    index_start = response.text.find('"', index_start) + 1
    index_end = response.text.find('"', index_start)
    csrfmiddlewaretoken = response.text[index_start:index_end]
    datas = {
        'username': "admin",
        'password': "admin",
        'csrfmiddlewaretoken': csrfmiddlewaretoken
    }
    response = test_main.post("login", data=datas,
                              headers={'Cookie': f'csrftoken={token_sec}',
                                       'Content-Type': 'application/x-www-form-urlencoded'})

    cookie = response.request.headers.get('Cookie')
    response = test_main.get("profile", headers={'Cookie': cookie})
    with allure.step("Запрос отправлен, посмотрим код ответа"):
        assert response.status_code == 200, f"Неверный код ответа, получен {response.status_code}"
        assert response.text.find('<div class="card">') > 0, "Заказы не найдены"


@allure.feature('Вход на сайт')
@allure.story('Логин под админом')
def test_login(test_main):
    token_sec = _get_new_csrf_string()
    response = test_main.get('login', headers={'Cookie': f'csrftoken={token_sec}'})
    index_start = response.text.find('csrfmiddlewaretoken')
    index_start = response.text.find('value', index_start)
    index_start = response.text.find('"', index_start) + 1
    index_end = response.text.find('"', index_start)
    csrfmiddlewaretoken = response.text[index_start:index_end]
    datas = {
        'username': "admin",
        'password': "admin",
        'csrfmiddlewaretoken': csrfmiddlewaretoken
    }
    response = test_main.post("login", data=datas,
                              headers={'Cookie': f'csrftoken={token_sec}',
                                       'Content-Type': 'application/x-www-form-urlencoded'})
    with allure.step("Запрос отправлен, посмотрим код ответа"):
        assert response.status_code == 200, f"Неверный код ответа, получен {response.status_code}"


@allure.feature('Выход с сайта')
@allure.story('Логаут под админом')
def test_logout(test_main):
    token_sec = _get_new_csrf_string()
    response = test_main.get('login', headers={'Cookie': f'csrftoken={token_sec}'})
    index_start = response.text.find('csrfmiddlewaretoken')
    index_start = response.text.find('value', index_start)
    index_start = response.text.find('"', index_start) + 1
    index_end = response.text.find('"', index_start)
    csrfmiddlewaretoken = response.text[index_start:index_end]
    datas = {
        'username': "admin",
        'password': "admin",
        'csrfmiddlewaretoken': csrfmiddlewaretoken
    }
    response = test_main.post("login", data=datas,
                              headers={'Cookie': f'csrftoken={token_sec}',
                                       'Content-Type': 'application/x-www-form-urlencoded'})

    cookie = response.request.headers.get('Cookie')
    response = test_main.get('logout', headers={'Cookie': cookie})

    with allure.step("Запрос отправлен, посмотрим код ответа"):
        assert response.status_code == 200, f"Неверный код ответа, получен {response.status_code}"


@allure.feature('Тесты на поиска')
@allure.story('Переход на страницу выдачи результата')
def test_search_page(test_main):
    token_sec = _get_new_csrf_string()
    response = test_main.get('login', headers={'Cookie': f'csrftoken={token_sec}'})
    index_start = response.text.find('csrfmiddlewaretoken')
    index_start = response.text.find('value', index_start)
    index_start = response.text.find('"', index_start) + 1
    index_end = response.text.find('"', index_start)
    csrfmiddlewaretoken = response.text[index_start:index_end]
    response = test_main.get(f'search_result?csrfmiddlewaretoken={csrfmiddlewaretoken}&search=1',
                             headers={'Cookie': f'csrftoken={token_sec}'})
    with allure.step("Запрос отправлен, посмотрим код ответа"):
        assert response.status_code == 200, f"Неверный код ответа, получен {response.status_code}"


@allure.feature('Тесты на поиска')
@allure.story('Проверка возвращаемого значения')
def test_search_result(test_main):
    token_sec = _get_new_csrf_string()
    response = test_main.get('login', headers={'Cookie': f'csrftoken={token_sec}'})
    index_start = response.text.find('csrfmiddlewaretoken')
    index_start = response.text.find('value', index_start)
    index_start = response.text.find('"', index_start) + 1
    index_end = response.text.find('"', index_start)
    csrfmiddlewaretoken = response.text[index_start:index_end]
    response = test_main.get(f'search_result?csrfmiddlewaretoken={csrfmiddlewaretoken}&search=1',
                             headers={'Cookie': f'csrftoken={token_sec}'})
    with allure.step("Запрос отправлен, посмотрим код ответа"):
        assert response.status_code == 200, f"Неверный код ответа, получен {response.status_code}"
        assert response.text.find('<div class="card">') > 0, "Не найдены карточка продукта"


@allure.feature('Тесты на отображение')
@allure.story('На главной странице последние 5 объектов из бд')
def test_main_page(test_main):
    token_sec = _get_new_csrf_string()
    response = test_main.get('', headers={'Cookie': f'csrftoken={token_sec}'})

    index = response.text.find('<div class="card">')
    cycle = 0
    while index > 0:
        cycle += 1
        index += 1
        index = response.text.find('<div class="card">', index)

    with allure.step('Подсчет числв ракточек продуктов'):
        assert cycle == 5, f"Карточек насчитали {cycle} штук"


@allure.feature('Тесты на отображение')
@allure.story('На странице со всеми объектами находятся все объекты из бд')
def test_service_page(test_main, get_db):
    token_sec = _get_new_csrf_string()
    response = test_main.get('service', headers={'Cookie': f'csrftoken={token_sec}'})

    index = response.text.find('<div class="card">')
    cycle = 0
    while index > 0:
        cycle += 1
        index += 1
        index = response.text.find('<div class="card">', index)

    with allure.step('Подсчет числв ракточек продуктов'):
        assert cycle == 11, f"Карточек насчитали {cycle} штук"


@allure.feature('Работа с БД')
@allure.story('Создаем пользователя')
def test_create_user(get_db):
    user = User.objects.create(username='user4', email='user4@user.ru',
                               password='41395e829c2895bda6d1407a410c6a3b3c3d806371b76879e1aa7ef377552ae8',
                               image='avatars/kreed7.jpg')
    assert user.username == 'user4'


@allure.feature('Работа с БД')
@allure.story('Получаем пользователя')
def test_get_user(get_db):
    user = User.objects.create(username='user4', email='user4@user.ru',
                               password='41395e829c2895bda6d1407a410c6a3b3c3d806371b76879e1aa7ef377552ae8',
                               image='avatars/kreed7.jpg')
    assert user.username == 'user4'
    people = User.objects.all()
    assert people[0].id == 1


@allure.feature('Работа с БД')
@allure.story('Получаем продукт')
def test_get_product(get_db):
    product = Product.objects.create(title='product1', description='description product1', image='avatars/kreed7.jpg')
    assert product.title == 'product1'
    products = Product.objects.all()
    assert products[0].title == 'product1'


@allure.feature('Работа с БД')
@allure.story('Создаем заказ')
def test_create_product(get_db):
    user = User.objects.create(username='user4', email='user4@user.ru',
                               password='41395e829c2895bda6d1407a410c6a3b3c3d806371b76879e1aa7ef377552ae8',
                               image='avatars/kreed7.jpg')
    assert user.username == 'user4'
    _user = User.objects.get(id=1)

    product = Product.objects.create(title='product1', description='description product1', image='avatars/kreed7.jpg')
    assert product.title == 'product1'
    _product = Product.objects.get(id=1)

    order = Order.objects.create(user=_user, product=_product)
    assert order.id == 1
    orders = Order.objects.all()
    assert orders[0].id == 1
