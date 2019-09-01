from rest_framework.pagination import PageNumberPagination


class GoodsPagination(PageNumberPagination):
    """
    商品列表自定义分页
    """

    # 默认每页显示的个数
    page_size = 12
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 每页最多能显示的个数
    max_page_size = 100
