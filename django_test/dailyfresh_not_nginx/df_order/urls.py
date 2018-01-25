from django.conf.urls import url
from df_order import views

urlpatterns = [
    url(r'^place/$', views.order_place), # 显示提交订单页面
]
