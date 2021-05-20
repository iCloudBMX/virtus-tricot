from django.db import models
from datetime import datetime

class BotUser(models.Model):
    chat_id = models.IntegerField()
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=50, blank=True)
    lang = models.CharField(max_length=10, default="uz")
    step = models.IntegerField(default=-1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Foydalanuvchilar"
        verbose_name = "Foydalanuvchi"


class Category(models.Model):
    name_uz = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name_uz
    
    class Meta:
        verbose_name_plural = "Kategoriyalar"
        verbose_name = "Kategoriya"


class Product(models.Model):
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True)
    image_id = models.TextField(default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name_plural = "Mahsulotlar"
        verbose_name = "Mahsulot"


class Order(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.name
    
    class Meta:
        verbose_name_plural = "Buyurtmalar"
        verbose_name = "Buyurtma"
        get_latest_by = 'id'