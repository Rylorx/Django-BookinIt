from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from books.models import Book

# Create your models here.

def validate_profile_image(value):
    extension = value.name.split(".")[-1].lower()
    
    # Can change this parameter later, just want to make sure my AWS S3 storage is not bombarded
    if value.file.size > 5*1024*1024:
        raise ValidationError("Image file too large ( > 1mb )")
    if extension != ".jpg":
        raise ValidationError("Image file must be of type .jpg")
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to="uploads/", validators=[validate_profile_image], blank=True, null=True)
    reading_goal = models.PositiveIntegerField(null=True, blank=True)
    display_reading_goal = models.BooleanField(default=False)

    # Optional Additional Parameters: , blank=True, null=True
    
    def __str__(self):
        return f"Profile of user: {self.user.username}"

class UserBook(models.Model):
    STATUS_CHOICES = (
        ('read', 'Read'),
        ('want_to_read', 'Want to Read'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'book', 'status')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     else:
#         instance.profile.save()
    