
class UrlPathRecordMiddleware(object):
    '''用户访问url地址记录中间件类'''
    exclude_path = ['/user/login/', '/user/register/', '/user/logout/']
    # ajax发起的请求也不记录 request.is_ajax()
    # 获取用户访问的url地址 request.path
    # http://127.0.0.1:8001/user/address/?a=1  /user/address/
    # 1.没有登录之前
    # a) 访问/user/address/, pre_url_path:/user/address/
    # b) 重定向访问/user/login/  pre_url_path:/user/address/
    # c) 输入用户名和密码，点击登录 /user/login_check/  pre_url_path:/user/address/
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        '''记录用户访问的地址'''
        if request.path not in UrlPathRecordMiddleware.exclude_path and not request.is_ajax():
            # 记录这个地址
            request.session['pre_url_path'] = request.path