# -*- encoding:utf-8 -*-
from django.db import models
from PIL import Image
from weimei import settings

# Create your models here.


class Fabric(models.Model):
    name = models.CharField(max_length=20, verbose_name="面料", default="棉", null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "面料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=20, verbose_name="品牌", null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Style(models.Model):
    name = models.CharField(max_length=30, verbose_name="特点", default="标准", null=False,unique=True)

    class Meta:
        verbose_name = "特点"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SizeToStyle(models.Model):
    name = models.IntegerField(verbose_name="尺码", choices=((70,'70'), (75,'75'), (80,'80'),(85,'85'), (90,'90'), (95,'95')))
    style = models.ForeignKey(Style,verbose_name="特点",related_query_name='sizes',related_name='size',on_delete=models.CASCADE)

    class Meta:
        verbose_name = "尺码和特点"
        verbose_name_plural = verbose_name
        unique_together = ("name","style")

    def __str__(self):
        template = '{0.name} {0.style.name}'
        return template.format(self)


class Season(models.Model):
    name = models.CharField(max_length=20,verbose_name="季节",unique=True)
    index = models.IntegerField(null= False,default=1)

    class Meta:
        verbose_name = "季节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Clothes(models.Model):
    name = models.CharField(verbose_name='名称',max_length=20,blank=False,default='K1',unique=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, related_name='clothes', related_query_name='clothes', verbose_name="品牌")
    fabric = models.ForeignKey(Fabric,on_delete=models.CASCADE,related_name='clothes',related_query_name='clothes', verbose_name="面料")
    sleeve = models.CharField(max_length=20,verbose_name="袖型",
                              choices=(("长袖","长袖"),("中袖","中袖"),("短袖","短袖"),("背心","背心")),null=False,
                              blank=False)
    size_to_styles = models.ManyToManyField(SizeToStyle, related_name="clothes", related_query_name="clothes",
                                           verbose_name="尺码及特点")
    price = models.IntegerField(verbose_name="价格")
    sold = models.IntegerField(verbose_name="销量",default=1000)
    seasons = models.ManyToManyField(Season, related_name="clothes", related_query_name="clothes",verbose_name="季节")
    update_time = models.DateField(auto_now_add=True,verbose_name='上传时间')
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数")
    click_nums = models.IntegerField(default=0,verbose_name="点击数")


    class Meta:
        verbose_name = "款型"
        verbose_name_plural = verbose_name

    def __str__(self):
        template = '{0.name} {0.brand.name} {0.fabric.name} {0.sleeve} '
        return template.format(self)


class Color(models.Model):
    name = models.CharField(max_length=20, verbose_name="颜色", default="黑色", null=False, blank=False)
    flower = models.CharField(max_length=120, verbose_name="花型", default="", null=False, blank=False)
    def color_path(self, filename):
        return 'image/clothes/big/color_{0}/{1}'.format(self.name, filename)

    colorImg = models.ImageField(upload_to=color_path, default="image/default.jpg", max_length=100, verbose_name='图片')
    #small image mid image big image

    clothing = models.ForeignKey(Clothes,verbose_name="款型",related_query_name='colors',related_name='colors',on_delete=models.CASCADE)

    class Meta:
        verbose_name = "款型颜色管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,%s"% (self.clothing,self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        #可以用异步resize和save但是得获取event_loop和装载tasks忒麻烦了
        import os
        filename = os.path.split(self.colorImg.name)[1]
        sizes = [(600, 800),(300, 400),(60, 80)]
        big_path = '{0}/image/clothes/big/color_{1}/{2}'.format(settings.MEDIA_ROOT,self.name, filename)
        mid_path = '{0}/image/clothes/mid/color_{1}/{2}'.format(settings.MEDIA_ROOT,self.name, filename)
        small_path = '{0}/image/clothes/small/color_{1}/{2}'.format(settings.MEDIA_ROOT,self.name, filename)
        paths = [big_path,mid_path,small_path]
        try:
            im = Image.open(big_path)
            for size,path in zip(sizes,paths):
                folder = os.path.exists(os.path.split(path)[0])
                if not folder:
                    os.makedirs(os.path.split(path)[0])
                im.resize(size).save(path)
        except IOError:
            pass


