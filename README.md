# Binance Orders

Binance Orders - это веб-приложение, которое позволяет создать number ордеров с общим объемом volume, каждый из которых 
имеет цену в диапазоне от priceMin до priceMax, и разброс объема каждого ордера amountDif. 
Приложение предоставляет API для взаимодействия с API Binance.


## Установка

1. Клонируйте репозиторий:

  ```shell
   git clone https://github.com/your-username/binance-orders.git
  ```
   
2. Установите зависимости проекта:
    
  ```shell
    cd binance-orders
    poetry install
  ```

3. Запустите миграции:
    
  ```shell
    make mm
   ```

4. Отредактируйте файл .env и укажите ваш API Key и Secret Key. Используйте тестовые ключи. Получить тестовые ключи можно по ссылке: https://testnet.binance.vision/

## Запуск

  ```shell
    make run
  ```

Приложение теперь будет доступно по адресу http://localhost:8000

## Эндпоинты:

http://localhost:8000/api/create_orders/

Пример POST запроса:

  ```shell
curl -X POST -H "Content-Type: application/json" -d '{
  "volume": 10000.0,
  "number": 5,
  "amountDif": 50.0,
  "side": "SELL",
  "priceMin": 200.0,
  "priceMax": 300.0
  }' http://localhost:8000/api/create_orders/
  ```