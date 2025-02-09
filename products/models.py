from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    ssn = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def disable(self):
        self.is_active = False
        self.save()
    
    def restore(self):
        self.is_deleted = False
        self.is_active = True
        self.save()

    def __str__(self):
        return self.title
