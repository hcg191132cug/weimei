from datetime import datetime

from django.db import models

# Create your models here.

class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name="标题")
    image = models.ImageField(upload_to='image/banner/%Y/%m',verbose_name="轮播图")
    url = models.URLField(max_length=200,verbose_name="访问地址")
    index = models.IntegerField(default=100,verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title