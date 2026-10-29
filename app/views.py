import os
from datetime import date, timedelta, datetime
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from app.models import *
from .models import HealthData
from django.contrib import messages
from django.views import View
# Create your views here.


def login_decorator(func):
    def wrap(request, *args, **kwargs):
        username = request.session.get('username')
        if username:
            a = func(request, *args, **kwargs)
            return a
        else:
            messages.warning(request, '登录信息已经过期，重新登录')
            return HttpResponse("<script> window.top.location.href='/login/?method=get'; </script>")
    return wrap

# class TestView(View):
#     def dispatch(self, request, *args, **kwargs):
#         # 方法一
#         # if request.method == "GET":
#         #     return self.get(request)
#         #
#         # elif request.method == "POST":
#         #     return self.post(request)
#         # 方法二 http://localhost:8000/login/?method=test
#         # method = request.GET.get('method')
#         # if method == "GET":
#         #     return self.get(request)
#         # elif method == "POST":
#         #     return self.post(request)
#         # elif method == "test":
#         #     return self.test(request)
#         # 方法三
#         # method = request.GET.get('method')
#         # return getattr(self,method)(request)
#
#         method = request.GET.get("method")
#         if not method:
#             return HttpResponse("缺少method参数")
#         method = method.lower()
#         allow_methods = {"get", "post"}
#         if method not in allow_methods:
#             return HttpResponse("不允许调用该方法")
#         if hasattr(self, method):
#             func = getattr(self, method)
#             return func(request)
#         return HttpResponse("方法不存在")

    # def get(self, request):
    #     return render(request, 'login.html')
    # def post(self, request):
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     # 存储用户信息
    #     request.session['username'] = username
    #
    #     if Admins.objects.filter(username=username, password=password):
    #         return redirect('/index/')
    #     else:
    #         return render(request, 'login.html', {'msg': '用户名或密码错误'})
    # def test(self, request):
    #     return HttpResponse("ok")

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 存储用户信息
        request.session['username'] = username

        if Admins.objects.filter(username=username,password=password):
            return redirect('/index/')
        else:
            return render(request,'login.html',{'msg':'用户名或密码错误'})
@login_decorator
def index(request):
    return render(request,'index.html')
@login_decorator
def dashboard(request):
    return render(request,'dashboard.html')
@login_decorator
def top(request):
    username = request.session.get('username', '')
    return render(request,'top.html', {'username': username})
@login_decorator
def left(request):
    return render(request,'left.html')

# 老人列表
@login_decorator
def elderlist(request):
    elderlist = Elder.objects.all()
    return render(request,'pages/elder-info.html',{'elderlist':elderlist})


# 根据姓名查询老人信息
@login_decorator
def getelderbyname(request):
    name = request.POST.get('name')
    # ORM
    elder = Elder.objects.filter(name=name)
    if elder:
        return HttpResponse("ok")
    return HttpResponse("no")

# 添加老人信息
@login_decorator
def elderadd(request):
    if request.method == 'GET':
        return render(request,'feature/addElder.html')
    else:
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        contact = request.POST.get('contact')
        relatives = request.POST.get('relatives')
        phone = request.POST.get('phone')
        healthcondition = request.POST.get('healthcondition')
        photo_obj = request.FILES.get('photo')
        if photo_obj is not None:
            # 获取文件名
            photo_name = photo_obj.name
            # 得到存储路径
            photo_path = "static/img"
            # 组装完整路径
            photo = os.path.join(photo_path,photo_name)
            # 将图片上传到指定文件夹
            with open(photo,'wb+') as image:
                for chunk in photo_obj.chunks():
                    image.write(chunk)
                photo = "/" + photo
        Elder.objects.create(
            name=name,
            age=age,
            gender=gender,
            contact=contact,
            phone=phone,
            healthcondition=healthcondition,
            relatives=relatives,
            photo=photo
        )
        return redirect('/elderlist/')


# 删除老人信息
@login_decorator
def elderdel(request):
        id = request.GET.get('id')
        Elder.objects.get(id=id).delete()
        return redirect('/elderlist/')

# 获得详细详细
@login_decorator
def elderGetByid(request):
    id = request.GET.get('id')
    elder = Elder.objects.get(id=id)
    return render(request,'feature/Elderselect.html',{'elder':elder})

# 修改数据
@login_decorator
def elderupdate(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        elder = Elder.objects.get(id=id)
        return render(request,'feature/Elderupdate.html',{'elder':elder})
    else:
        id = request.POST.get('id')
        elder = Elder.objects.get(id=id)
        elder.name = request.POST.get('name')
        elder.age = request.POST.get('age')
        elder.gender = request.POST.get('gender')
        elder.contact = request.POST.get('contact')
        elder.relatives = request.POST.get('relatives')
        elder.phone = request.POST.get('phone')
        elder.healthcondition = request.POST.get('healthcondition')
        elder.photo_obj = request.FILES.get('photo')
        if elder.photo_obj is not None:
            # 获取文件名
            photo_name = elder.photo_obj.name
            # 得到存储路径
            photo_path = "static/img"
            # 组装完整路径
            photo = os.path.join(photo_path, photo_name)
            # 将图片上传到指定文件夹
            with open(photo, 'wb+') as image:
                for chunk in elder.photo_obj.chunks():
                    image.write(chunk)
                photo = "/" + photo
            elder.photo = photo
        else:
            photo = request.POST.get('old_photo')
            elder.photo = photo
        elder.save()
        return redirect('/elderlist/')
@login_decorator
def getHealthDataByDate(request):
    date = request.POST.get('date')
    healthDataList = HealthData.objects.filter(recordTime__contains=date).values('id','bloodPressure','bloodSugar','heartRate','bloodOxygen','temperature','weight','recordTime','elder__name')
    return JsonResponse(list(healthDataList), safe=False)

# 健康数据
@login_decorator
def healthdata(request):

    nowdate = date.today()
    healthData = HealthData.objects.filter(recordTime__contains=nowdate)  # date.today（）这一天的数据库中所有的数据对象
    return render(request,'pages/health-data.html',{'healthdata':healthData,'nowdate':nowdate})
    # # 健康数据页面
    # 查询表里所有健康数据
    # all_health = HealthData.objects.all()
    # # 把数据传给前端页面
    # return render(request, 'pages/health-data.html', {"healthdata": all_health})

# # 健康数据导入
@login_decorator
def healthdataadd(request):
    if request.method == 'GET':
        elderlist = Elder.objects.all()
        return render(request, 'feature/health-data-add.html', {'elderlist': elderlist})
    else:
        elder_id = request.POST.get('id')
        bloodPressure = request.POST.get('bloodPressure')
        bloodSugar = request.POST.get('bloodSugar')
        heartRate = request.POST.get('heartRate')
        bloodOxygen = request.POST.get('bloodOxygen')
        temperature = request.POST.get('temperature')
        weight = request.POST.get('weight')
        recordTime =request.POST.get('recordTime')
    HealthData.objects.create(
        elder_id=elder_id,
        bloodPressure=bloodPressure,
        bloodSugar=bloodSugar,
        heartRate=heartRate,
        bloodOxygen=bloodOxygen,
        temperature=temperature,
        weight=weight,
        recordTime=recordTime,
    )
    return redirect('/healthdata/')

# 健康数据删除
@login_decorator
def healthdatadel(request):
    id = request.GET.get('id')
    HealthData.objects.get(id=id).delete()
    return redirect('/healthdata/')

# 修改数据
@login_decorator
def healthdataupdate(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        healthdata = HealthData.objects.get(id=id)
        return render(request, 'feature/health-data-update.html', {'healthdata': healthdata})
    else:
        id = request.POST.get('id')
        healthdata = HealthData.objects.get(id=id)
        healthdata.bloodPressure = request.POST.get('bloodPressure')
        healthdata.bloodSugar = request.POST.get('bloodSugar')
        healthdata.heartRate = request.POST.get('heartRate')
        healthdata.bloodOxygen = request.POST.get('bloodOxygen')
        healthdata.temperature = request.POST.get('temperature')
        healthdata.weight = request.POST.get('weight')
        healthdata.recordTime = request.POST.get('recordTime')
        healthdata.save()
        return redirect('/healthdata/')



# 行为轨迹
@login_decorator
def camerainfo(request):
    return render(request,'pages/camera-info.html')
# 健康阈值设置
@login_decorator
def threshold(request):
    return render(request,'pages/threshold.html')


# def get_dailyreport_context(request):
#     # 1.从URL GET参数获取查询条件（搜索关键词、报告类型）
#     #  搜索框input:  name=keyword
#     keyword = request.GET.get('keyword', '').strip()  # 查询的关键字
#     # 报告类型：查询框关键字:name = report_type
#     report_type = request.GET.get('report_type', '').strip()
#
#     # 2.查询Report报告表，select_related做外键预加载，关联elder老人表，避免N+1查询
#     # report_list是惰性QuerySet对象，不是列表，不会立刻执行SQL；只有模板循环渲染的时候才真正执行数据库查询。
#     # report_list = Report.objects.select_related('elder').all()
#
#     # 什么也没输入输出全部的信息
#     report_list = Report.objects.all()
#
#     # 3.如果传入keyword关键词，多条件模糊搜索：报告名称 或者 老人姓名
#     if keyword:
#         q1 = report_list.filter(report_name__icontains=keyword)  # A | B 满足A或者B的条件 大小写不敏感  filter(条件1，条件2)where
#         # q1 = report_list.filter(report_name__contains=keyword)  # A | B 满足A或者B的条件 大小写敏感  __contains包含关系 like
#         q2 = report_list.filter(elder__name__icontains=keyword)
#         report_list = q1 | q2
#         # report_list = report_list.filter(
#         #     Q(report_name__icontains=keyword) | Q(elder__name__icontains=keyword)  # A | B 满足A或者B的条件 大小写不敏感
#         # )
#     # 4.如果传入report_type，按报告类型模糊过滤
#     if report_type:
#         report_list = report_list.filter(report_type__icontains=report_type)
#
#     # 5.日期计算：今天、本周周一（周起始）
#     today = date.today()  # 只有年月日
#     #  本周 周一的天数
#     week_start = today - timedelta(days=today.weekday())  # weekday()周一=0，周日=6  timedelta得到天数
#
#     # 全部老人列表
#     elderlist = Elder.objects.all()
#
#     # --------统计指标，三次独立数据库查询--------
#     # 今日生成报告总数
#     today_report_count = Report.objects.filter(create_time__date=today).count()  # __date 忽略时分秒只取今天的时间
#     # 本周（周一到今天）报告总数 __gte大于等于   __lte小于等于
#     week_report_count = Report.objects.filter(create_time__date__gte=week_start, create_time__date__lte=today).count()
#     # 异常报告：状态不等于'已生成'全部算作异常
#     abnormal_report_count = Report.objects.exclude(status='已生成').count()
#
#     # 返回字典，作为模板上下文，传给前端模板渲染
#     return {
#         'report_list': report_list,      # 过滤后的报告查询集,    什么也没输入得到全部数据
#         'elderlist': elderlist,          # 全部老人 得到名字
#         'today': today,                  # 当前日期，页面回显
#         'keyword': keyword,              # 回显搜索框关键词
#         'report_type': report_type,      # 回显筛选报告类型
#         'today_report_count': today_report_count,    #今日报告数量统计
#         'week_report_count': week_report_count,      #本周报告数量统计
#         'abnormal_report_count': abnormal_report_count #异常报告数量
#     }
def daily_report_view(request):
    # 1.从URL GET参数获取查询条件（搜索关键词、报告类型）
    #  搜索框input:  name=keyword
    keyword = request.GET.get('keyword', '').strip()  # 查询的关键字
    # 报告类型：查询框关键字:name = report_type
    report_type = request.GET.get('report_type', '').strip()

    # 2.查询Report报告表report_list是惰性QuerySet对象，不是列表，不会立刻执行SQL；只有模板循环渲染的时候才真正执行数据库查询。
    # 什么也没输入输出全部的信息
    report_list = Report.objects.all()

    # 3.如果传入keyword关键词，多条件模糊搜索：报告名称 或者 老人姓名
    if keyword:
        q1 = report_list.filter(report_name__icontains=keyword)  # A | B 满足A或者B的条件 大小写不敏感  filter(条件1，条件2)where
        # q1 = report_list.filter(report_name__contains=keyword)  # A | B 满足A或者B的条件 大小写敏感  __contains包含关系 like
        q2 = report_list.filter(elder__name__icontains=keyword)
        report_list = q1 | q2
        # report_list = report_list.filter(
        #     Q(report_name__icontains=keyword) | Q(elder__name__icontains=keyword)  # A | B 满足A或者B的条件 大小写不敏感
        # )
    # 4.如果传入report_type，按报告类型模糊过滤
    if report_type:
        report_list = report_list.filter(report_type__icontains=report_type)
    # 5.日期计算：今天、本周周一（周起始）
    today = date.today()  # 只有年月日
    #  本周 周一的天数
    week_start = today - timedelta(days=today.weekday())  # weekday()周一=0，周日=6  timedelta得到天数

    # 全部老人列表
    elderlist = Elder.objects.all()
    # --------统计指标，三次独立数据库查询--------
    # 今日生成报告总数
    today_report_count = Report.objects.filter(create_time__date=today).count()  # __date 忽略时分秒只取今天的时间
    # 本周（周一到今天）报告总数 __gte大于等于   __lte小于等于
    week_report_count = Report.objects.filter(create_time__date__gte=week_start, create_time__date__lte=today).count()
    # 异常报告：状态不等于'已生成'全部算作异常
    abnormal_report_count = Report.objects.exclude(status='已生成').count()
    # 构造上下文字典
    context = {
        'report_list': report_list,      # 过滤后的报告查询集,    什么也没输入得到全部数据
        'elderlist': elderlist,          # 全部老人 得到名字
        'today': today,                  # 当前日期，页面回显
        'keyword': keyword,              # 回显搜索框关键词
        'report_type': report_type,      # 回显筛选报告类型
        'today_report_count': today_report_count,    #今日报告数量统计
        'week_report_count': week_report_count,      #本周报告数量统计
        'abnormal_report_count': abnormal_report_count #异常报告数量
    }
    # 返回渲染模板，替换为你的模板文件名，例如 "daily_report.html"
    return render(request, "feature/daily-report.html", context)
# 日常报告生成
def dailyreport(request):
    report_list = Report.objects.all()
    elderlist = Elder.objects.all()
    return render(request, 'feature/daily-report.html', {'report_list':report_list,'elderlist': elderlist } )

# 新增日常报告
def dailyreportadd(request):
    if request.method == 'GET':
        return render(request, 'feature/daily-report.html')
    else:

        report_no = request.POST.get("report_no")  # b编号
        report_name = request.POST.get("report_name")  # 报告名称
        elder_id = request.POST.get("elder_id")  # 外键赋值用 _id     外键id
        report_type = request.POST.get("report_type")  # 报告类型
        create_time = request.POST.get("report_date")  # 时间
        file_format = request.POST.get("format")  # 文件类型
        status = request.POST.get("status")  # 状态
        file_path = request.POST.get("file_path")  #路径
        Report.objects.create(
            report_no = report_no
            ,report_name = report_name
            ,elder_id = elder_id
            ,report_type = report_type
            ,create_time = create_time
            ,file_format = file_format
            ,file_path = file_path
            ,status = status
        )
        return redirect('/dailyreport/')
# 修改日常报告
def dailyreportupdate(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        report = Report.objects.get(id=id)
        elderlist = Elder.objects.all()
        return render(request,'feature/daily-report-update.html',{'report':report,'elderlist':elderlist})
    else:
        id = request.POST.get('id')
        report = Report.objects.get(id=id)
        report.report_no = request.POST.get("report_no")  # b编号
        report.report_name = request.POST.get("report_name")  # 报告名称
        report.elder_id = request.POST.get("elder_id")  # 外键赋值用 _id     外键id
        report.report_type = request.POST.get("report_type")  #报告类型
        report.create_time = request.POST.get("report_date")  # 时间
        report.file_format = request.POST.get("format")  #文件类型
        report.status = request.POST.get("status")  # 状态
        # report.file_path = request.POST.get("file_path")  #路径
        report.save()
        return redirect('/dailyreport/')

# 日常报告删除
def dailyreportdel(request):
    id = request.GET.get('id')
    Report.objects.get(id=id).delete()
    return redirect('/dailyreport/')
# 行为记录管理
def behaviorrecord(request):
    return render(request,'feature/behavior-record.html')








def book(request):
    return render(request,'book.html')



