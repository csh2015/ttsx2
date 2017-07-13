#coding=utf-8
from haystack import indexes
from models import GoodsInfo
#指定对于某个类的某些数据建立索引
class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

# 对这个类进行搜索
    def get_model(self):
        return GoodsInfo    # 实际的模型类

    def index_queryset(self, using=None):
        return self.get_model().objects.all()    #所有数据