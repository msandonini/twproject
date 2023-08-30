from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


class Review(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opera = models.ForeignKey('mediapop.Media', on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='reviews/')
    vote = models.DecimalField(max_digits=3, decimal_places=1,
                               validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    text = models.TextField()

    def __str__(self):
        return self.title


class ReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    vote = models.DecimalField(max_digits=3, decimal_places=1,
                               validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f"Commento di @{self.user.username} sulla recensione '{self.review.title}'"
