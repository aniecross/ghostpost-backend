from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    boast = models.BooleanField(default=True)
    text = models.CharField(max_length=140)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    create_at = models.DateTimeField(default=timezone.now)
    
    @property
    def score(self):
        return self.like - self.dislike