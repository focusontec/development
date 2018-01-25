from django.shortcuts import render
from django.core.paginator import Paginator # 导入分页类
from df_goods.models import Goods,Image
from df_goods.enums import *
from df_user.models import BrowseHistory
# Create your views here.


# http://127.0.0.1:8000
def home_list_page(request):
    '''显示首页内容'''
    # 1.查询水果的4个商品和3个新品
    fruits = Goods.objects.get_goods_by_type(goods_type_id=FRUIT, limit=4)
    fruits_new = Goods.objects.get_goods_by_type(goods_type_id=FRUIT, limit=3, sort='new')
    seafood = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=4)
    seafood_new = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=3, sort='new')
    meat = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=4)
    meat_new = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=3, sort='new')
    eggs = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=4)
    eggs_new = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=3, sort='new')
    vegetables = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=4)
    vegetables_new = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=3, sort='new')
    frozen = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=4)
    frozen_new = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=3, sort='new')
    # 2.组织上下文数据
    context = {'fruits':fruits, 'fruits_new':fruits_new,
               'seafood':seafood, 'seafood_new':seafood_new,
               'meat':meat, 'meat_new':meat_new,
               'eggs':eggs, 'eggs_new':eggs_new,
               'vegetables':vegetables, 'vegetables_new':vegetables_new,
               'frozen':frozen, 'frozen_new':frozen_new}
    return render(request, 'df_goods/index.html', context)


# /goods/商品id/
def goods_detail(request, goods_id):
    '''显示商品详情页面'''
    # 1.根据商品id查询商品信息
    # 方法1
    # goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    # 获取商品的详情图片
    # images = Image.objects.get_image_by_goods_id(goods_id=goods_id)
    # 方法2
    # goods = Goods.objects.get_goods_by_id_with_image(goods_id=goods_id)
    # 方法3
    goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
    # 2.根据商品类型查询新品信息
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # todo: 添加历史浏览记录
    # 如果用户未登录，不需要添加历史浏览记录。
    if request.session.has_key('islogin'):
        passport_id = request.session.get('passport_id')
        BrowseHistory.objects.add_one_history(passport_id=passport_id, goods_id=goods_id)

    # 3.使用模板文件
    type_title = GOODS_TYPE[goods.goods_type_id]
    context = {'goods':goods, 'goods_new':goods_new,
               'type_title':type_title}
    return render(request, 'df_goods/detail.html', context)


# /list/类型id/页码/?sort=排序方式
def goods_list(request, goods_type_id, pindex):
    '''显示商品列表页面'''
    # 获取排序方式
    sort = request.GET.get('sort', 'default')
    # 根据goods_type_id查询商品信息
    goods_li = Goods.objects.get_goods_by_type(goods_type_id=goods_type_id, sort=sort)

    # 进行分页操作
    paginator = Paginator(goods_li, 1)

    # 获取第pindex页的内容
    pindex = int(pindex)
    goods_li = paginator.page(pindex) # 返回值是一个Page对象

    # 获取分页之后的总页数
    nums_pages = paginator.num_pages
    # 控制页码列表
    if nums_pages < 5:
        # 如果不足5页，页码全显示
        pages = range(1, nums_pages+1)
    elif pindex <= 3:
        # 当前页是前3页，显示前5页
        pages = range(1, 6)
    elif nums_pages - pindex <= 2: # 10 9 8 7
        # 当前页是后3页，显示后5页
        pages = range(nums_pages-4 ,nums_pages+1)
    else:
        # 其他情况，显示当前页的前两页和后两页，当前页
        pages = range(pindex-2, pindex+3)

    # 根据商品类型查询新品信息
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods_type_id, limit=2, sort='new')

    # 定义上下文
    context = {'goods_li':goods_li, 'type_id':goods_type_id,
               'sort':sort, 'type_title':GOODS_TYPE[int(goods_type_id)],
               'pages':pages, 'goods_new':goods_new}
    # 使用模板文件
    return render(request, 'df_goods/list.html', context)