from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from orders.models import Order


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    biography = models.TextField(default='Tell us about yourself')
    preferences = models.TextField(default='Describe your travel preferences')

    def get_orders(self):
        return Order.objects.filter(user=self.user)

    def get_orders_with_details(self):
        orders = Order.objects.filter(user=self.user)
        order_details = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            order_details.append({'order': order, 'items': order_items})
        for order_detail in order_details:
            for item in order_detail['items']:
                item.product_name = Product.objects.get(id=item.product_id).name
        return order_details

    def __str__(self):
        return f'{self.user.username} Profile'  # show how we want it to be displayed

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
