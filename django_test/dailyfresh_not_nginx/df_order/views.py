from django.shortcuts import render
from df_cart.models import Cart
from df_user.models import Address
from utils.decorators import login_required
from django.views.decorators.http import require_GET,require_POST,require_http_methods
# Create your views here.
# /order/place/
@require_POST
@login_required
def order_place(request):
    '''显示提交订单页面'''
    cart_id_list = request.POST.getlist('cart_id_list')
    # print(cart_id_list)
    # 查询id在cart_id_list列表中购物车记录　
    cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
    # 获取用户的默认收货地址
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_one_address(passport_id=passport_id)
    return render(request, 'df_order/place_order.html', {'cart_list':cart_list, 'addr':addr})
