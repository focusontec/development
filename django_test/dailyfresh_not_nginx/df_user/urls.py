from django.conf.urls import url
from  df_user import views

urlpatterns = [
    url(r'^register/$', views.register), # 显示注册页面
    # url(r'^register_handle/$', views.register_handle), # 用户注册
    url(r'^check_user_exist/$', views.check_user_exist), # 校验用户名是否存在

    url(r'^login/$', views.login), # 显示登录页面
    url(r'^login_check/$', views.login_check), # 登录校验
    url(r'^logout/$', views.logout), # 退出登录

    url(r'^$', views.user), # 显示用户中心-个人信息页
    url(r'^address/$', views.address), # 显示用户中心-个人地址页
    url(r'^order/$', views.order),  # 显示用户中心-个人订单页
]
