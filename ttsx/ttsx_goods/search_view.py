# coding=utf-8
from haystack.generic_views import SearchView

class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        # 调用父类的方法，来对上下文进行设置
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['cart_show'] = '1'
        page_list=[]    # 创建列表
        page_obj=context['page_obj']   #先拿到page_obj对象，
        if page_obj.paginator.num_pages<5:     #小于5页
            page_list=range(1,page_obj.paginator.num_pages+1)   #页码从1开始，到当前页码
        elif page_obj.number<=2:    #如果当前页小于等于2页
            page_list=range(1,5+1)
        # 如果大于等于倒数第二页
        elif page_obj.number>=page_obj.paginator.num_pages-1:# 6 7 8 9 10
            page_list=range(page_obj.paginator.num_pages-5+1,page_obj.paginator.num_pages+1)
        else:
            page_list=range(page_obj.number-2,page_obj.number+3)
        context['page_list']=page_list    # 将值返回带html页面当中
        return context
