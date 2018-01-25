from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseManager
from django.db.models import Sum # 导入Sum聚合类
from df_goods.models import Goods
# Create your models here.


class CartManager(BaseManager):
    '''购物车模型管理器类'''
    def get_one_cart_info(self, passport_id, goods_id):
        '''判断用户购物车中是否添加过该商品'''
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return cart_info

    def add_one_cart_info(self, passport_id, goods_id, goods_count):
        '''添加商品到购物车'''
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        if cart_info:
            # 1.如果用户购物车中添加过该商品，更新商品数量
            total_count = cart_info.goods_count + goods_count
            # 判断商品库存
            if total_count <= goods.goods_stock:
                #　库存充足
                cart_info.goods_count = total_count
                cart_info.save()
                return True
            else:
                # 库存不足
                return False
        else:
            # 2.如果用户购物车中没有添加过该商品，创建新记录
            # 判断商品库存
            if goods_count <= goods.goods_stock:
                # 库存充足
                self.create_one_object(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
                return True
            else:
                # 库存不足
                return False

    def get_cart_count_by_passport(self, passport_id):
        '''获取购物车中商品的总数'''
        # select sum(goods_count) form s_cart where passport_id=passport_id
        res_dict = self.filter(passport_id=passport_id).aggregate(Sum('goods_count'))
        # {'goods_count__sum':值}
        # {'goods_count__sum':None}
        res = res_dict['goods_count__sum']
        if res is None:
            res = 0
        return res

    def get_cart_list_by_passport(self, passport_id):
        '''获取用户的购物车记录信息'''
        cart_list = self.get_object_list(filters={'passport_id':passport_id})
        return cart_list

    def update_one_cart_info(self, passport_id, goods_id, goods_count):
        '''更新用户购物车中商品的数目'''
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        # 判断商品库存
        if goods_count <= cart_info.goods.goods_stock:
            # 库存充足
            cart_info.goods_count = goods_count
            cart_info.save()
            return True
        else:
            # 库存不足
            return False

    def del_one_cart_info(self, passport_id, goods_id):
        '''删除购物车中对应记录'''
        # 数据库操作的代码，应该放在try...except中间
        # 防止操作数据库时发送异常
        try:
            cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
            cart_info.delete()
            return True
        except:
            return False

    def get_cart_list_by_id_list(self, cart_id_list):
        '''获取id在cart_id_list中购物车记录'''
        # self.filter(id__in=cart_id_list)
        cart_list = self.get_object_list(filters={'id__in':cart_id_list})
        return cart_list


class Cart(BaseModel):
    '''购物车模型类'''
    passport = models.ForeignKey('df_user.Passport', verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')
    goods_count = models.IntegerField(default=1, verbose_name='商品数目')

    objects = CartManager()

    class Meta:
        db_table = 's_cart'
