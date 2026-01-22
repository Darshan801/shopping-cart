from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField( max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=200, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available =models.BooleanField(default=True)
    category =models.ForeignKey(Category,on_delete=models.CASCADE) # the product attached with the category will be deleted with on_delete
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

# to get url that redirect to the product_detail page
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
class variationManager(models.Manager):
    def colors(self):
        return super(variationManager, self).filter(variation_category = 'color' , is_active=True)
    
    def sizes(self):
        return super(variationManager, self).filter(variation_category = 'size' , is_active=True)
    

Variation_category_choice=(
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=50 , choices=Variation_category_choice)
    variation_value=models.CharField(max_length=50)
    is_active= models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)
    
    objects = variationManager()

    def __str__(self):
        return self.variation_value #to get string value instead of objects