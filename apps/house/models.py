from django.utils import timezone as datetime

from django.db import models


class Community(models.Model):
    """
    小区
    """
    id = models.BigIntegerField(default=0, unique=True, verbose_name="小区id")
    title = models.CharField(default=0, primary_key=True, max_length=50, verbose_name="小区名称")
    link = models.CharField(default=0, max_length=255, unique=True, verbose_name="链接地址")
    district = models.CharField(default=0, max_length=50, verbose_name="区域")
    bizcircle = models.CharField(default=0, max_length=50, verbose_name="商圈")
    tagList = models.CharField(default=0, max_length=50, verbose_name="地铁站")
    onsale = models.IntegerField(default=0, verbose_name="在售房屋数量")
    onrent = models.IntegerField(default=0, null=True, verbose_name="在租房屋数量")
    year = models.IntegerField(default=0, null=True, verbose_name="建造年份")
    housetype = models.CharField(default=0, max_length=50, null=True, verbose_name="房屋类型")
    cost = models.CharField(default=0, max_length=50, null=True, verbose_name="物业费")
    service = models.CharField(default=0, max_length=50, null=True, verbose_name="物业公司")
    company = models.CharField(default=0, max_length=50, null=True, verbose_name="开发商")
    building_num = models.IntegerField(default=0, null=True, verbose_name="楼房栋数")
    house_num = models.IntegerField(default=0, null=True, verbose_name="房屋总数")
    price = models.FloatField(default=0, null=True, verbose_name="平均价格")
    city = models.CharField(default=0, max_length=50, null=True, verbose_name="城市")

    validdate = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "小区"
        verbose_name_plural = verbose_name


class Houseinfo(models.Model):
    """
    房源信息
    """
    houseID = models.BigIntegerField(default=0, primary_key=True, verbose_name="房子id")
    title = models.CharField(default=0, max_length=50, verbose_name="房子名称")
    link = models.CharField(default=0, max_length=255, verbose_name="房子链接")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name="小区名称")
    years = models.IntegerField(default=0, verbose_name="建成时间")
    housetype = models.CharField(default=0, max_length=50, verbose_name="房屋类型")
    square = models.FloatField(default=0, max_length=50, verbose_name="房屋面积")
    direction = models.CharField(default=0, max_length=50, verbose_name="朝向")
    floor = models.CharField(default=0, max_length=50, verbose_name="楼层")
    taxtype = models.CharField(default=0, max_length=50, verbose_name="标签")
    totalPrice = models.FloatField(default=0, verbose_name="总价")
    unitPrice = models.FloatField(default=0, verbose_name="每平米价格")
    followInfo = models.CharField(default=0, max_length=50, verbose_name="关注数")
    decoration = models.CharField(default=0, max_length=50, verbose_name="装饰类型")
    houseState = models.CharField(max_length=50, verbose_name='房源状态', default='在售')
    updatedate = models.DateTimeField(default=datetime.now, verbose_name='成交时间')
    validdate = models.DateTimeField(default=datetime.now, verbose_name='插入数据时间')

    class Meta:
        verbose_name = "房源信息"
        verbose_name_plural = verbose_name


# class Sellinfo(models.Model):
#     """
#     成交房源信息
#     """
#     houseID = models.IntegerField(primary_key=True, verbose_name="房屋id")
#     title = models.CharField(max_length=50, verbose_name="房子名称")
#     link = models.CharField(max_length=50, verbose_name="房子链接")
#     community = models.ForeignKey(Community, on_delete=models.CASCADE)
#     years = models.IntegerField(verbose_name="建成时间")
#     housetype = models.CharField(max_length=50, verbose_name="房屋类型")
#     square = models.FloatField(max_length=50, verbose_name="房屋面积")
#     direction = models.CharField(max_length=50, verbose_name="朝向")
#     floor = models.CharField(max_length=50, verbose_name="楼层")
#     totalPrice = models.FloatField(verbose_name="总价")
#     unitPrice = models.FloatField(verbose_name="每平米价格")
#     dealdate = models.CharField(max_length=50, null=True, verbose_name="成交时间")
#
#     class Meta:
#         verbose_name = "成交房源信息"
#         verbose_name_plural = verbose_name


class Rentinfo(models.Model):
    """
    租房信息
    """
    houseID = models.BigIntegerField(default=0, primary_key=True, verbose_name="房子id")
    title = models.CharField(default=0, max_length=50, verbose_name="房子名称")
    link = models.CharField(default=0, max_length=255, verbose_name="房子链接")
    decoration = models.CharField(default=0, max_length=50, verbose_name="装饰类型")
    region = models.CharField(default=0, max_length=50, verbose_name="区域")
    zone = models.CharField(default=0, max_length=50, verbose_name="商圈")
    meters = models.FloatField(default=0, verbose_name="平米数")
    other = models.CharField(default=0, max_length=50, verbose_name="其他信息")
    subway = models.CharField(default=0, max_length=50, verbose_name="地铁站")
    heating = models.CharField(default=0, max_length=50, verbose_name="供暖")
    price = models.FloatField(default=0, max_length=50, verbose_name="单价")
    housetype = models.CharField(default=0, max_length=50, verbose_name="户型")
    updatedate = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "租房信息"
        verbose_name_plural = verbose_name


class Hisprice(models.Model):
    """
    房屋总价
    """
    houseID = models.BigIntegerField(default=0, primary_key=True, verbose_name="房子id")
    totalPrice = models.FloatField(default=0, verbose_name="总价")
