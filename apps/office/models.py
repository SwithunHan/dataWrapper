from django.db import models


# Create your models here.
class OfficeSkills(models.Model):
    name = models.CharField(max_length=50, verbose_name="技能要求", default="", unique=True, primary_key=True)

    class Meta:
        verbose_name = "技能"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OfficeType(models.Model):
    name = models.CharField(max_length=50, verbose_name="工作类型", default="", unique=True, primary_key=True)

    class Meta:
        verbose_name = "工作类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OfficeArea(models.Model):
    name = models.CharField(max_length=50, verbose_name="工作区域", default="", unique=True, primary_key=True)

    class Meta:
        verbose_name = "工作区域"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Company(models.Model):
    officeArea = models.ForeignKey(OfficeArea, verbose_name="工作区域", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="公司名称", default="")

    class Meta:
        verbose_name = "公司"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Office(models.Model):
    officeType = models.ForeignKey(OfficeType, verbose_name="工作类型", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name="公司", on_delete=models.CASCADE)
    skills = models.ManyToManyField(OfficeSkills, verbose_name="技能要求")
    experience = models.CharField(max_length=50, verbose_name="工作经验")
    salary = models.FloatField(verbose_name="薪资")

    class Meta:
        verbose_name = "工作信息"
        verbose_name_plural = verbose_name

    def get_skills(self):
        return "\n".join([s.name for s in self.skills.all()])
