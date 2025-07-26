# Импортируем необходимые библиотеки и переменные
import requests
from config import keys, API_KEY

# Обозначаем собственный класс ошибок для различия системных(отказ API) и неправильный ввод
class APIException(Exception):
    pass

# Испольуем staticmetod для вызова, без создания объекта
class CurrencyConverter:
    @staticmethod
    # Возвращаем число с плавающей точкой, принимая конвертирующуюся валюту, в конвертируемую валюту и количество соотвественно
    def get_price(base: str, quote: str, amount: str) -> float:
        # Проверяем одинаковые валюты
        if base == quote:
            raise APIException(f'Нельзя переводить одинаковые валюты: {base}')

        # Получаем коды валют в нижнем регистре
        try:
            base_code = keys[base.lower()]
            quote_code = keys[quote.lower()]
        except KeyError:
            raise APIException('Такой валюты нет в списке. Введите /values')

        # Проверяем количество
        try:
        # Чтобы можно было конвертировать дробное количество
            amount = float(amount)
        except ValueError:
            raise APIException('Количество должно быть числом')

        # Делаем запрос к API
        try:
            response = requests.get(
                f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base_code}/{quote_code}/{amount}'
            )
            # Преобразуем ответ в словарь Python
            data = response.json()

            # Проверяем успешность запроса
            if data.get('result') == 'success':
                return data['conversion_result']
            else:
                raise APIException('Ошибка при получении курса')

        except:
            raise APIException('Не удалось подключиться к серверу')