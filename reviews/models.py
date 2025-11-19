# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from reviews import admin
from django.utils import timezone


def validate_review_file(value):
    extension = value.name.split(".")[-1].lower()
    allowed_extensions = ["pdf", "txt", "jpg"]
    
    if value.file.size > 1024*1024:
        raise ValidationError("File too large ( > 1mb )")
    if extension not in allowed_extensions:
        raise ValidationError("File must be of type .pdf, .txt, or .jpg, other file types are not supported")

class BookReview(models.Model):
    GENRE_CHOICES = [
        ('FICT', 'Fiction'),
        ('NFICT', 'Non-Fiction'),
        ('SCI_FI', 'Science Fiction'),
        ('MYST', 'Mystery'),
        ('ROM', 'Romance'),
        ('THRILL', 'Thriller'),
        ('HORROR', 'Horror'),
        ('FANTASY', 'Fantasy'),
        ('BIOG', 'Biography'),
        ('HIST', 'Historical'),
        ('CHILD', 'Children'),
        ('OTHER', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_reviews')
    title = models.CharField(max_length=200) # 200
    author = models.CharField(max_length=100) # 100
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES, default='OTHER') # 10
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    # File upload field with metadata
    file_upload = models.FileField(
        upload_to="uploads/", 
        validators=[validate_review_file], 
        blank=True, 
        null=True
    )
    file_title = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
    )
    file_keywords = models.CharField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Keywords describing the file content"
    )
    file_description = models.TextField(
        blank=True, 
        null=True,
    )

    def __str__(self):
        return f"{self.title} - reviewed by {self.user.username}"

    class Meta:
        ordering = ['-date']  # Most recent reviews first

class BookReviewMembership(models.Model):
    review = models.ForeignKey(BookReview, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    joined_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('review', 'user')
        
    def __str__(self):
        return f"{self.user.username} is a member of {self.review.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(BookReview, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.title}"
    class Meta:
       ordering = ['-date'] 

class JoinRequest(models.Model):
    
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
        
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(BookReview, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requested to join {self.review.title}"
    
    # Ensures that a user can only request to join a review once
    # class Meta:
    #     unique_together = ('user', 'review')