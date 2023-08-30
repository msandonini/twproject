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
