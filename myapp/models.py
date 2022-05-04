from django.db import models
from django.contrib.auth.models import  User
from PIL import Image
from django.utils.html import  format_html
import datetime
# Create your models here.

class  Category(models.Model):
    name =models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.name

    @property
    def get_category_total(self):
        product = self.product_set.all()
        total = product.count()
        return total


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True)


    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if self.image:
            imag = Image.open(self.image.path).resize((1800,1120))
            imag.save(self.image.path)

    def __str__(self):
        return self.name

    def show_image_html(self):
        if self.image:
            return format_html('<img src="%s" height="40px" >' % self.image.url)
        else:
            return ''

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url

class Customer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=200, null=True)
    Last_Name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=10, null=True)
    image = models.ImageField(upload_to='upload/customer/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        if self.image:
            imag = Image.open(self.image.path).resize((1800,1120))
            imag.save(self.image.path)

    def show_image_html(self):
        if self.image:
            return format_html('<img src="%s" height="40px" >' % self.image.url)
        else:
            return ''

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url='/images/profile.png'
        return url

    def __str__(self):
        return self.First_Name + " " +  self.Last_Name


STATUS_CHOICE =(
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Complete', 'Complete'),
    ('Canceled', 'Canceled'),
)

TABLE_CHOICE =(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10')
)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    table_no =  models.CharField(max_length =30, choices=TABLE_CHOICE)
    status = models.CharField(max_length =30,  choices=STATUS_CHOICE)

    def __str__(self):
        return str(self.id)


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cert_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.id)



TIME_CHOICE =(
    ('11.00 - 11.45','11.00 - 11.45'),
    ('12.00 - 12.45','12.00 - 12.45'),
    ('13.00 - 13.45','13.00 - 13.45'),
    ('14.00 - 14.45','14.00 - 14.45'),
    ('15.00 - 15.45','15.00 - 15.45'),
    ('16.00 - 16.45','16.00 - 16.45'),
    ('17.00 - 17.45','17.00 - 17.45'),
    ('18.00 - 18.45','18.00 - 18.45'),
    ('19.00 - 19.45','19.00 - 19.45'),
    ('20.00 - 20.45','20.00 - 20.45'),
    ('21.00 - 21.45','21.00 - 21.45'),
    ('22.00 - 22.45','22.00 - 22.45'),
)



class BookTable(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_time = models.DateField('book table date')
    people = models.IntegerField(default=0, null=True, blank=True)
    message = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length =30,  choices=STATUS_CHOICE)
    timeBook = models.CharField('book table time', max_length =30,  choices=TIME_CHOICE)