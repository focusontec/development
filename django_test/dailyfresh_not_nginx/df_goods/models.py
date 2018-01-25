from django.db import models
from tinymce.models import HTMLField
from db.base_model import BaseModel
from db.base_manager import BaseManager
from df_goods.enums import *
# Create your models here.


class GoodsLogicManager(BaseManager):
    '''商品模型逻辑管理器类'''

    def get_goods_by_id(self, goods_id):
        '''根据商品id查询商品信息'''
        goods = self.get_one_object(id=goods_id)
        # 查询商品的详情图片
        images = Image.objects.get_image_by_goods_id(goods_id=goods_id)
        # 给goods对象增加一个属性images
        goods.images = images
        # 返回goods
        return goods


class GoodsManager(BaseManager):
    '''商品模型管理器类'''
    def get_goods_by_id_with_image(self, goods_id):
        '''根据商品id查询商品信息，包含商品详情图片'''
        goods = self.get_one_object(id=goods_id)
        # 查询商品的详情图片
        images = Image.objects.get_image_by_goods_id(goods_id=goods_id)
        # 给goods对象增加一个属性images
        goods.images = images
        # 返回goods
        return goods

    def get_goods_by_id(self, goods_id):
        '''根据商品id查询商品信息'''
        goods = self.get_one_object(id=goods_id)
        return goods

    def get_goods_by_type(self, goods_type_id, limit=None, sort='default'):
        '''根据商品类型id查询商品新鲜'''
        # sort='new'  查询新品 按照创建时间进行排序
        # sort='price' 按照价格进行排序
        # sort='hot' 按照销量进行排序
        order_by = ('-pk', )
        if sort == 'new':
            order_by = ('-create_time', )
        elif sort == 'price':
            order_by = ('goods_price', )
        elif sort == 'hot':
            order_by = ('-goods_sales', )

        goods_li = self.get_object_list(filters={'goods_type_id':goods_type_id}, order_by=order_by)
        if limit:
            # 对查询结果集进行切片
            goods_li = goods_li[:limit]
        return goods_li


class Goods(BaseModel):
    '''商品模型类'''
    '''
    goods_type_choice = (
        (1, '新鲜水果'),
        (2, '海鲜水产'),
        (3, '猪牛羊肉'),
        (4, '禽类蛋品'),
        (5, '新鲜蔬菜'),
        (6, '速冻食品')
    )
    '''
    goods_type_choice = (
        (FRUIT, GOODS_TYPE[FRUIT]),
        (SEAFOOD, GOODS_TYPE[SEAFOOD]),
        (MEAT, GOODS_TYPE[MEAT]),
        (EGGS, GOODS_TYPE[EGGS]),
        (VEGETABLES, GOODS_TYPE[VEGETABLES]),
        (FROZEN, GOODS_TYPE[FROZEN])
    )
    goods_type_id = models.SmallIntegerField(choices=goods_type_choice, default=FRUIT, verbose_name='商品类型')
    goods_name = models.CharField(max_length=20, verbose_name='商品名称')
    goods_sub_title = models.CharField(max_length=128, verbose_name='商品副标题')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品运费')
    goods_unite = models.CharField(max_length=10, verbose_name='商品单位')
    goods_info = HTMLField(verbose_name='商品描述')
    goods_image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    goods_stock = models.IntegerField(default=0, verbose_name='商品库存')
    goods_sales = models.IntegerField(default=0, verbose_name='商品销量')
    # 0:下线商品 1:上线商品
    '''
    goods_status_choice = (
        (0, '下线商品'),
        (1, '上线商品')
    )
    '''
    goods_status_choice = (
        (OFFLINE, GOODS_STATUS[OFFLINE]),
        (ONLINE, GOODS_STATUS[ONLINE])
    )
    goods_status = models.SmallIntegerField(choices=goods_status_choice, default=ONLINE, verbose_name='商品状态')

    objects = GoodsManager() # 如果不需要商品详情图片
    objects_logic = GoodsLogicManager() # 需要商品详情图片

    class Meta:
        db_table = 's_goods'


class ImageManager(BaseManager):
    '''商品详情图片模型管理器类'''
    def get_image_by_goods_id(self, goods_id):
        '''根据商品id获取商品详情图片'''
        images = self.get_object_list(filters={'goods_id':goods_id}) # QuerySet
        # 取出一张图片
        if images.exists():
            # 有图片
            images = images[0] # Image类的对象
        return images # 可能是一个QuerySet,也可能是一个Image


class Image(BaseModel):
    '''商品详情图片模型类'''
    goods = models.ForeignKey('Goods', verbose_name='所属商品')
    img_url = models.ImageField(upload_to='goods', verbose_name='详情图片')

    objects = ImageManager()

    class Meta:
        db_table = 's_goods_image'












