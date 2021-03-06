# Generated by Django 2.1.7 on 2019-04-22 18:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigIntegerField(default=0, unique=True, verbose_name='小区id')),
                ('title', models.CharField(default=0, max_length=50, primary_key=True, serialize=False, verbose_name='小区名称')),
                ('link', models.CharField(default=0, max_length=255, unique=True, verbose_name='链接地址')),
                ('img_link', models.CharField(default=0, max_length=255, unique=True, verbose_name='图片链接')),
                ('district', models.CharField(default=0, max_length=50, verbose_name='区域')),
                ('bizcircle', models.CharField(default=0, max_length=50, verbose_name='商圈')),
                ('tagList', models.CharField(default=0, max_length=50, verbose_name='地铁线路')),
                ('subStation', models.CharField(default=0, max_length=50, verbose_name='地铁站')),
                ('web_sign', models.IntegerField(default=0, verbose_name='网签数量')),
                ('onsale', models.IntegerField(default=0, verbose_name='在售房屋数量')),
                ('onrent', models.IntegerField(default=0, null=True, verbose_name='在租房屋数量')),
                ('year', models.IntegerField(default=0, null=True, verbose_name='建造年份')),
                ('housetype', models.CharField(default=0, max_length=50, null=True, verbose_name='房屋类型')),
                ('cost', models.CharField(default=0, max_length=50, null=True, verbose_name='物业费')),
                ('service', models.CharField(default=0, max_length=50, null=True, verbose_name='物业公司')),
                ('company', models.CharField(default=0, max_length=50, null=True, verbose_name='开发商')),
                ('building_num', models.IntegerField(default=0, null=True, verbose_name='楼房栋数')),
                ('house_num', models.IntegerField(default=0, null=True, verbose_name='房屋总数')),
                ('price', models.FloatField(default=0, null=True, verbose_name='平均价格')),
                ('city', models.CharField(default=0, max_length=50, null=True, verbose_name='城市')),
                ('validdate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小区',
                'verbose_name_plural': '小区',
            },
        ),
        migrations.CreateModel(
            name='Hisprice',
            fields=[
                ('houseID', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='房子id')),
                ('totalPrice', models.FloatField(verbose_name='总价')),
            ],
        ),
        migrations.CreateModel(
            name='Houseinfo',
            fields=[
                ('houseID', models.BigIntegerField(default=0, primary_key=True, serialize=False, verbose_name='房子id')),
                ('title', models.CharField(default=0, max_length=50, verbose_name='房子名称')),
                ('link', models.CharField(default=0, max_length=255, verbose_name='房子链接')),
                ('years', models.IntegerField(default=0, verbose_name='建成时间')),
                ('housetype', models.CharField(default=0, max_length=50, verbose_name='房屋类型')),
                ('square', models.FloatField(default=0, max_length=50, verbose_name='房屋面积')),
                ('direction', models.CharField(default=0, max_length=50, verbose_name='朝向')),
                ('floor', models.CharField(default=0, max_length=50, verbose_name='楼层')),
                ('tag', models.CharField(default=0, max_length=50, verbose_name='标签')),
                ('totalPrice', models.FloatField(default=0, verbose_name='总价')),
                ('unitPrice', models.FloatField(default=0, verbose_name='每平米价格')),
                ('followInfo', models.CharField(default=0, max_length=50, verbose_name='关注数')),
                ('decoration', models.CharField(default=0, max_length=50, verbose_name='装饰类型')),
                ('houseState', models.CharField(default='在售', max_length=50, verbose_name='房源状态')),
                ('updatedate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='成交时间')),
                ('validdate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='插入数据时间')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.Community', verbose_name='小区名称')),
            ],
            options={
                'verbose_name': '在售房源信息',
                'verbose_name_plural': '在售房源信息',
            },
        ),
        migrations.CreateModel(
            name='Rentinfo',
            fields=[
                ('houseID', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='房子id')),
                ('title', models.CharField(max_length=50, verbose_name='房子名称')),
                ('link', models.CharField(max_length=50, verbose_name='房子链接')),
                ('decoration', models.CharField(max_length=50, verbose_name='装饰类型')),
                ('region', models.CharField(max_length=50, verbose_name='区域')),
                ('zone', models.CharField(max_length=50, verbose_name='商圈')),
                ('meters', models.FloatField(verbose_name='平米数')),
                ('other', models.CharField(max_length=50, verbose_name='其他信息')),
                ('subway', models.CharField(max_length=50, verbose_name='地铁站')),
                ('heating', models.CharField(max_length=50, verbose_name='供暖')),
                ('price', models.FloatField(max_length=50, verbose_name='单价')),
                ('housetype', models.CharField(max_length=50, verbose_name='户型')),
                ('updatedate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': '租房信息',
                'verbose_name_plural': '租房信息',
            },
        ),
    ]
