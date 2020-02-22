from django.urls import path

from stockgetweb.stock import views

app_name = 'stock'
urlpatterns = [
    path(
        'stockFilter/',
        view=views.StockFilterView.as_view(),
        name='stockFilter'),
]
