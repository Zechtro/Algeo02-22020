from django.db import models

# Create your models here.
class ImageInput(models.Model):
    image = models.ImageField(upload_to='inputimage/',null=True)
    result = models.IntegerField(default=0)
    search_time = models.DecimalField(default=0, max_digits=9, decimal_places=3)
    
    def delete(self):
        self.image.delete()
        super().delete()
    
class ImageDataset(models.Model):
    image = models.ImageField(upload_to='dataset/',null=True)
    similarity = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=9)