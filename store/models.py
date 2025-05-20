from django.db import models
from django.utils import timezone

# المنتج
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # دي الصورة الرئيسية

    def __str__(self):
        return self.name

# الصور الإضافية للمنتج
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_gallery/')

    def __str__(self):
        return f"صورة إضافية لـ {self.product.name}"

# الطلب
class Order(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"طلب من {self.full_name} - {self.product.name}"

# زيارات الموقع
class SiteVisit(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"زيارات يوم {self.date} - {self.count} زيارة"
