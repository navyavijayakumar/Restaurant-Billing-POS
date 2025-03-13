from django.db import models

# Create your models here.
class Table(models.Model):
    title=models.CharField(max_length=50)
    status=models.BooleanField(default=True)

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    title=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    category_object=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")

    def __str__(self):
        return self.title
    
class Order(models.Model):
    status=models.BooleanField(default=False)
    phone=models.CharField(max_length=15)
    table_object=models.ForeignKey(Table,on_delete=models.CASCADE,related_name="orders")

class OrderItems(models.Model):
    qty=models.DecimalField(max_digits=7,decimal_places=3)
    order_object=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product_obj=models.ForeignKey(Product,on_delete=models.CASCADE)
