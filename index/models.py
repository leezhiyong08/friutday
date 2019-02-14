from django.db import models

# Create your models here.
class Users(models.Model):
    uphone=models.CharField(max_length=20,verbose_name='电话号码')
    upwd=models.CharField(max_length=20,verbose_name='密码')
    uemail=models.EmailField(verbose_name='电子邮件')
    uname=models.CharField(max_length=20,verbose_name='用户名')
    isActive=models.BooleanField(default=True,verbose_name='是否激活')

    def __str__(self):
        return self.uphone

    def to_dic(self):
        dic = {
            "id":self.id,
            "uphone": self.uphone,
            "upwd": self.upwd,
            "uemail": self.uemail,
            "isActive": self.isActive
        }
        return dic


class GoodsType(models.Model):
    title = models.CharField(max_length=50, verbose_name='类型名称')
    picture = models.ImageField(upload_to='static/upload/goods', null=True, verbose_name='类型图片')
    desc=models.TextField(verbose_name='商品描述')

    def __str__(self):
        return self.title

    def to_dic(self):
        dic={
            'title':self.title,
            'picture':self.picture.__str__(),
            'desc':self.desc,
        }
        return dic

    class Meta:
        db_table='GoodType'
        verbose_name='商品类型'
        verbose_name_plural=verbose_name

class Goods(models.Model):
    title=models.CharField(max_length=40,verbose_name='商品名称')
    price=models.DecimalField(max_digits=7,decimal_places=2,verbose_name='商品价格')
    spec=models.CharField(max_length=30,verbose_name='规格')
    picture=models.ImageField(upload_to='static/upload/goods',null=True,verbose_name='商品图片')
    goodsType=models.ForeignKey(GoodsType,verbose_name='商品类型')
    isActive=models.BooleanField(default=True,verbose_name='是否上架')

    def __str__(self):
        return self.title

    class Meta:
        db_table='Goods'
        verbose_name='商品'
        verbose_name_plural=verbose_name