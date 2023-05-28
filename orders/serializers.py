from rest_framework import serializers


class CreateOrdersSerializer(serializers.Serializer):
    volume = serializers.FloatField()
    number = serializers.IntegerField()
    amountDif = serializers.FloatField()
    side = serializers.ChoiceField(choices=["SELL", "BUY"])
    priceMin = serializers.FloatField()
    priceMax = serializers.FloatField()
