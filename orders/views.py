import os
import random

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.serializers import CreateOrdersSerializer

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

client = Client(api_key, api_secret, testnet=True)


class CreateOrdersView(APIView):
    def post(self, request):
        serializer = CreateOrdersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        volume = data["volume"]
        number = data["number"]
        amount_dif = data["amountDif"]
        side = data["side"]
        price_min = data["priceMin"]
        price_max = data["priceMax"]

        order_volume = volume / number
        response_data = []

        for i in range(number):
            price = random.uniform(price_min, price_max)
            volume_dif = random.uniform(-amount_dif, amount_dif)
            actual_volume = order_volume + volume_dif
            actual_volume = round(actual_volume, 2)

            try:
                if side == "SELL":
                    order = create_sell_order(actual_volume, price)
                elif side == "BUY":
                    order = create_buy_order(actual_volume, price)

                response_data.append(
                    {
                        "order_id": order["order_id"],
                        "symbol": order["symbol"],
                        "side": order["side"],
                        "quantity": order["quantity"],
                        "price": order["price"],
                    }
                )
            except Exception as e:
                return Response({"error": str(e)}, status=400)

        return Response({"orders": response_data}, status=201)


def create_sell_order(volume, price):
    try:
        order = client.create_order(
            symbol="BTCUSDT",
            side="SELL",
            type="LIMIT",
            timeInForce="GTC",
            quantity=volume,
            price=price,
        )

        print("Ордер успешно создан:")
        print(order)

        return order

    except BinanceAPIException as e:
        print("Ошибка API Binance:", e)

    except BinanceOrderException as e:
        print("Ошибка создания ордера:", e)


def create_buy_order(volume, price):
    try:
        order = client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="LIMIT",
            timeInForce="GTC",
            quantity=volume,
            price=price,
        )

        print("Ордер успешно создан:")
        print(order)

        return order

    except BinanceAPIException as e:
        print("Ошибка API Binance:", e)

    except BinanceOrderException as e:
        print("Ошибка создания ордера:", e)
