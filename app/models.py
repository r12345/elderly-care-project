from django.db import models

# Create your models here.
class Admins(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    status = models.IntegerField(default=0)  # 0表示超级管理员 1表示普通管理员
# 老人信息
class Elder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.IntegerField()  # 0男 1女
    healthcondition = models.CharField(max_length=50)  # 健康状况
    contact = models.CharField(max_length=30)  # 紧急联系人
    relatives = models.CharField(max_length=30)  # 亲属关系
    phone = models.CharField(max_length=11)
    photo = models.CharField(max_length=255)

# 健康信息
class HealthData(models.Model):
    id = models.AutoField(primary_key=True)
    bloodPressure = models.CharField(max_length=20)  # 血压
    bloodSugar = models.FloatField()  # 血糖
    heartRate = models.FloatField()  # 心率
    bloodOxygen = models.FloatField()  # 血氧
    temperature = models.FloatField()  # 体温
    weight = models.FloatField()  # 体重
    recordTime = models.DateTimeField()  # 记录时间
    # 设置一个外键
    # to="Elder": 指定这个外键关联到Elder模型
    # on_delete=models.SET_NULL: 定义了当被关联的Elder对象被删除时，当前模型中的elder字段应该如何处理
    # models.SET_NULL: 表示当被关联的Elder对象被删除时，当前模型的elder字段值会被设置为NULL
    # null=True: 必须和SET_NULL一起使用。它允许elder字段在数据库中存储NULL值
    elder = models.ForeignKey(to="Elder",on_delete=models.SET_NULL,null=True)


class Report(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    report_no = models.CharField(max_length=32, verbose_name="报告编号")  # 报告编号 RPT20260806001
    report_name = models.CharField(max_length=100, verbose_name="报告名称")  # 报告名称
    # 外键关联老人，一个老人有多份报告
    elder = models.ForeignKey(
        to="Elder",
        on_delete=models.CASCADE,  # 老人删除，级联删除报告；也可SET_NULL
        related_name="report_list",
        verbose_name="所属老人"
    )
    # 报告类型：健康数据 / 综合日报 / 行为活动 / 睡眠质量
    report_type = models.CharField(max_length=32, verbose_name="报告类型")
    # 生成时间
    create_time = models.DateTimeField(verbose_name="生成时间")
    # 文件格式 PDF / Word / Excel
    file_format = models.CharField(max_length=16, verbose_name="文件格式")
    # 状态：已生成 / 生成中
    status = models.CharField(max_length=16, verbose_name="状态")
    # 可选：文件存储路径
    file_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="文件路径")

    class Meta:
        verbose_name = "报告"
        verbose_name_plural = verbose_name
        ordering = ['-create_time']  # 默认按生成时间倒序
