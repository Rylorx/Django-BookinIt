from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    publisher = models.CharField(max_length=200)
    date_published = models.DateField()
    img_url = models.URLField(max_length=500, null=True)
    buy_link = models.URLField(max_length=500, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
