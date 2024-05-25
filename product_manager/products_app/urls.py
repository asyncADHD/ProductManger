from django.urls import path
from .views import (home, product_list, product_create, product_update, product_delete, price_history,
                    get_historical_data, product_update_name)

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
    path('products/create/', product_create, name='product_create'),
    path('products/update/<int:pk>/', product_update, name='product_update'),
    path('products/delete/<int:pk>/', product_delete, name='product_delete'),
    path('price_history/', price_history, name='price_history'),
    path('historical_data/<int:product_id>/', get_historical_data, name='historical_data'),
    path('products/update_name/', product_update_name, name='product_update_name'),
]
