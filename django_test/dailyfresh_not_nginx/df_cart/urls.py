from django.conf.urls import url
from df_cart import views

urlpatterns = [
    url(r'^add/$', views.cart_add), # 添加商品到购物车
    url(r'^count/$', views.cart_count), # 获取购物车中的商品的总数
    url(r'^$', views.cart_show), # 显示购物车页面
    url(r'^update/$', views.cart_update), # 更新购物车商品数目
    url(r'^del/$', views.cart_del), # 删除购物车记录
]
