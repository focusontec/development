from haystack import indexes
# 导入你的模型类
from df_goods.models import Goods

# 指定对于某个类的某些数据建立索引
# 索引类的名字：模型类名+Index
class GoodsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 返回你的模型类
        return Goods

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
