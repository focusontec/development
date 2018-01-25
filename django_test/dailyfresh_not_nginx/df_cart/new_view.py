from django.shortcuts import render

from django.http import JsonResponse
from utils.decorators import login_required
from django.views.decorators.http import require_http_methods,require_GET,require_POST
from df_cart.models import Cart

@require_GET
@login_required
def cart_add(request):
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    #2 . 添加商品到购物车
    res = Cart.objects.add_one_cart_info(passport_id= passport_id,goods_id= goods_id,goods_count=int(goods_count))
    if res:
        return JsonResponse({'res':1})
    return JsonResponse({'res':0})


