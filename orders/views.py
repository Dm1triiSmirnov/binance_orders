import os
import random

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.serializers import CreateOrdersSerializer

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

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
            price = round(price, 8)
            volume_dif = random.uniform(-amount_dif, amount_dif)
            actual_volume = order_volume + volume_dif
            actual_volume = round(actual_volume, 8)

            try:
                if side == "SELL":
                    min_price, max_price = get_price_range("ETHUSDT", "SELL")
                elif side == "BUY":
                    min_price, max_price = get_price_range("ETHUSDT", "BUY")
                else:
                    raise ValueError("Invalid side")

                if price < min_price or price > max_price:
                    return Response(
                        {
                            "error": "Price does not meet the filter requirements for the selected side"
                        },
                        status=400,
                    )

                order = create_order(symbol="ETHUSDT", side=side, quantity=actual_volume, price=price)

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


def get_price_range(symbol, side):
    symbol_info = client.get_symbol_info(symbol)
    percent_price_filter = next(filter(lambda f: f["filterType"] == "PERCENT_PRICE", symbol_info["filters"]))
    min_price_percent = float(percent_price_filter["multiplierDown"])
    max_price_percent = float(percent_price_filter["multiplierUp"])
    current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])

    if side == "SELL":
        min_price = current_price * (1 - min_price_percent)
        max_price = current_price * (1 - max_price_percent)
    else:
        min_price = current_price * (1 + min_price_percent)
        max_price = current_price * (1 + max_price_percent)

    return min_price, max_price


def create_order(symbol, side, quantity, price):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price,
        )

        print("Ордер успешно создан:")
        print(order)

        return order

    except BinanceAPIException as e:
        print("Ошибка API Binance:", e)

    except BinanceOrderException as e:
        print("Ошибка создания ордера:", e)
