from django import forms
from .models import BookReview, Comment

class BookReviewForm(forms.ModelForm):
    file_title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    file_keywords = forms.CharField(
        max_length=500,
        required=False,
        help_text="Enter keywords separated by commas",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., fiction, mystery, thriller'
        })
    )
    file_description = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )

    class Meta:
        model = BookReview
        fields = [
            'title', 'author', 'genre', 'comment', 'rating',
            'file_upload', 'file_title', 'file_keywords', 'file_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'file_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file_upload(self):
        file_upload = self.cleaned_data.get("file_upload")
        if file_upload:
            extension = file_upload.name.split(".")[-1].lower()
            allowed_extensions = ["pdf", "txt", "jpg"]
            if extension not in allowed_extensions:
                raise forms.ValidationError("File must be of type .pdf, .txt, or .jpg, other file types are not supported")
        return file_upload

    def clean_file_keywords(self):
        keywords = self.cleaned_data.get("file_keywords")
        if keywords:
            # Strip whitespace from each keyword and filter out empty strings
            keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
            return ','.join(keyword_list)
        return keywords

class BookSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for review or file by title, genre, author, or keyword...'
        })
    )

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Add a comment'
    )
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        label='Rating',
        min_value=1, max_value=5
    )

    class Meta:
        model = Comment
        fields = ['text', 'rating']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = [
            'title', 'author', 'genre', 'comment', 'rating',
            'file_upload', 'file_title', 'file_keywords', 'file_description'
        ]
