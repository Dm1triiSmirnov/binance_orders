from django.urls import path

from orders.views import CreateOrdersView

urlpatterns = [
    path("create_orders/", CreateOrdersView.as_view(), name="create_orders"),
]
