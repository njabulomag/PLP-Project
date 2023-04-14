from django.db import models
from django.contrib.auth.models import User
import datetime

class SoftDeleteModel(models.Model):

    deleted_at = models.DateTimeField(null=True, default=None)

    def soft_delete(self):
        self.deleted_at = datetime.datetime.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True

class Category(SoftDeleteModel):
    name = models.CharField(max_length=300, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Picture(SoftDeleteModel):
    image = models.ImageField(upload_to='pictures')
    date_posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='General', blank=True)
    
    def __str__(self):
        return self.image.name
    

   