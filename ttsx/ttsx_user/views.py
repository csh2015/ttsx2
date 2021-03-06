# coding=utf-8
from django.shortcuts import render , redirect
from models import UserInfo
from hashlib import sha1
from django.http import JsonResponse
import datetime
import user_decorators
from ttsx_goods.models import GoodsInfo

# Create your views here.

def register(request):     # 注册第一步，呈现模板
    context = {'title':'注册','top':'0'}        #将此处的值传递给模板页面
    return render(request,'ttsx_user/register.html',context)

# 接收并处理注册信息
def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    ucpwd = post.get('user_cpwd')
    uemail = post.get('user_email')

    context={}
    # 如果考虑html页面禁用，来源于客户端的验证可能不准确，最好再验证一次，所有的验证信息都要再做一次判断
    # 这里只做了一次判断
    if len(uname)<5 or len(uname)>20:
        context['error_name'] = '请输入5-20个字符的用户'
        context['uname'] = uname
        return render(request,'ttsx_user/register.html',context)

    else:
        # 用sha1进行加密
        s1 = sha1()    # 创建对象
        s1.update(upwd)
        upwd_sha1 = s1.hexdigest()

        user = UserInfo()   # 创建对象
        user.uname = uname    # 将接收到的值通过models传给数据库
        user.upwd = upwd_sha1   # 存储加密之后的值
        user.umail = uemail
        user.save()      # 向数据库中保存数据

        return redirect('/user/login/')    # 注册完成之后，页面自动跳转到登陆页面


# 接收用户名
def register_valid(request):
    # 接收用户名
    uname = request.get.GET.get('uname')
    #js当中用post请求接收验证之后，此处也需要修改接收数据的方式
    # uname = request.get.POST.get('uname')
    # 查询当前用户的个数
    data = UserInfo.objects.filter(uname=uname).count()
    # 返回json{‘valid’:1或0}
    context ={'valid':data}
    return JsonResponse(context)    # 给回调函数传值为valid


# d登陆页面
def login(request):
    # 从页面当中取出在login_handle中保存的cookie值
    uname = request.COOKIES.get('uname','')  # 默认值为空字符串，为了防止没有输入用户名时显示None

    context={'title':'登陆','uname':uname,'top':'0'}
    return render(request,'ttsx_user/login.html',context)


# 上传登陆信息
def login_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    # 记住密码按钮
    ujz = post.get('user_jz',0)     # 在值还没有传递过来之前，默认值为0，表示不用记住，只有在登陆成功的时候需要记住


    s1 = sha1()
    s1.update(upwd)
    upwd_sha1= s1.hexdigest()

    context = {'title': '登陆' ,'uname':uname,'upwd':upwd ,'top':'0'}   #此处top是指用来判断是否继承模板的

    # POST:如果没有查到数据，则返回[],如果查到数据则返回[UserInfo]
    # GET:如果查到了返回的就是一个UserInfo对象，不是一个列表，如果没有查到，则抛出异常
    result = UserInfo.objects.filter(uname=uname)     #从数据库中查找数据
    if len(result)==0:
        # 用户名不存在
        context['error_name'] = '用户名错误'
        return render(request,'ttsx_user/login.html',context)   # 当用户名错误时，返回的提示
    else:
        if result[0].upwd == upwd_sha1:
            #登陆成功
            # 因为redirect 是HttpResponseRedict的简写，所以HttpResponse有这个子类，所以直接redirect可以返回一个response对象
            response =  redirect(request.session.get('url_path','/'))  #登陆成功之后跳转到自定义页面,什么都不写的话进入到首页
            request.session['uid'] = result[0].id   #result[0].id是从数据库中查到的用户id,用session保存用户的id用于后面用户中心获得用户信息
            request.session['uname'] = result[0].uname    # 将用户名存储在session中，用于模板中显示时调用
            # 记住用户名，因为用户名不属于保密信息，所以可以用cookie存储在浏览器中
            if ujz =='1':     #所有从请求报文中接受的对象都是字符串
                response.set_cookie('uname',uname,expires=datetime.datetime.now()+ datetime.timedelta(days=14))     #可以调用response的set_cookie方法，值可以在每个用户的浏览器中去存储
            else:      #如果取消勾选记住用户名  ,则用户名立即过期
                response.set_cookie('uname',uname,max_age=-1)
            return response    #依然可以跳转页面
        else:
            #密码错误
            context['error_pwd'] = '密码错误'      # 视图向模板中传递的变量，可以在模板中进行判断
            return render(request,'ttsx_user/login.html',context)    # 当密码错误时，返回的提示

# 退出就是清除session
def logout(request):
    request.session.flush()
    return redirect('/user/login/')    # 退出转向到登陆页面

# 以下三个视图需要登陆验证，此处应该使用装饰器来进行验证

def islogin(request):
    result = 0   #默认为0
    if request.session.has_key('uid'):
        result = 1  # 如果已经登陆，则返回1
    return JsonResponse({'islogin':result})  #返回一个字典,用于list.html中ajax中的回调函数的参数data

# 用户中心
@user_decorators.user_islogin
def center(request):
    # 查询当前登陆的用户对象
    user = UserInfo.objects.get(pk = request.session['uid'])
    # 查询最近浏览
    ids = request.COOKIES.get('goods_ids','').split(',')[:-1]    #此处信息被切分为[1,2,3]
    glist = []      #此处建立一个列表来存储id号，否则是按照默认升序来存储id号的
    for id in ids:
        glist.append(GoodsInfo.objects.get(id = id)) # 查询，在ids的范围内进行过滤，查到之后传递到模板当中

    context = {'user':user,'glist':glist}     #glist传递到模板当中去进行渲染
    return render(request,'ttsx_user/center.html',context)

# 订单页面
@user_decorators.user_islogin
def order(request):
    context = {}
    return render(request, 'ttsx_user/order.html', context)

# 收货信息
# 此视图函数用于两种功能：
# 第一种是页面跳转到收货信息页面时，通过get方法来获得用户信息，来进行收货信息的呈现，当没有填写收货信息时，则都为空
# 第二种是通过post方法，来获得表单提交的数据，保存于对应用户的数据库中
@user_decorators.user_islogin
def site(request):
    user = UserInfo.objects.get(pk = request.session['uid'])     # 创建user对象，获得用户信息

    # 此处是当用户填写收货地址并提交之后，会执行这一步判断，将收货信息数据存储在数据库中，并留做模板中的变量来调用
    # 此步是只有post请求时会执行这一步
    if request.method == 'POST':      # post请求，修改当前用户对象的收货请求
        post = request.POST
        # 接收在表单中填写的收货地址信息
        ushou = post.get('ushou')
        uaddress = post.get('uaddress')
        ucode = post.get('ucode')
        uphone = post.get('uphone')

        # 将对象属性进行赋值
        user.ushou = ushou
        user.uaddress = uaddress
        user.ucode = ucode
        user.uphone = uphone
        user.save()      # 将数据保存于数据库

    # 此处用于渲染模板内容，将保存于数据库中的数据通过视图传给模板，呈现出来,两种方法post和get都会调用这一步来呈现模板
    context  = {'user':user}
    return  render(request,'ttsx_user/site.html',context)
