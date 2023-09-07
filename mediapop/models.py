from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Media(models.Model):
    MEDIA_TYPES = (
        ('vg', 'Videogioco'),
        ('f', 'Film'),
        ('tv', 'Serie TV'),
        ('a', 'Anime')
    )

    name = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)

    def __str__(self):
        return self.name


class MediaVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    vote = models.IntegerField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    class Meta:
        unique_together = ('user', 'media')

    def __str__(self):
        return f"Valutazione di @{self.user.username} all'opera {self.media.name}"
