from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from reviews.models import BookReview, Comment
from allauth.socialaccount.models import SocialAccount
from .forms import UserDetailsForm, UserUpdateForm
from .models import Profile
from django.contrib.auth.models import User

def home(request):
    reviews = BookReview.objects.all().order_by("-date")[:10]
    user = request.user

    if user.is_authenticated:
        membership_ids = set(user.memberships.values_list("review_id", flat=True))
    else:
        membership_ids = set()

    context = {
        "first_name": user.first_name if user.is_authenticated else "Guest",
        "pma_flag": user.groups.filter(name="PMA").exists(),
        "reviews": reviews,
        "membership_ids": membership_ids,
    }
    return render(request, "home.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def user_profile(request):
    profile_user = request.user
    profile, created = Profile.objects.get_or_create(user=profile_user)
    reviews_written = profile_user.book_reviews.all()
    commented_reviews = BookReview.objects.filter(comments__user=profile_user).distinct()

    # get bookshelves
    books_read = profile_user.user_books.filter(status='read')
    books_want_to_read = profile_user.user_books.filter(status='want_to_read')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=profile_user)
        details_form = UserDetailsForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and details_form.is_valid():
            user_form.save()
            details_form.save()
            return redirect('user_profile')
    else:
        user_form = UserUpdateForm(instance=profile_user)
        details_form = UserDetailsForm(instance=profile)

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'reviews_written': reviews_written,
        'commented_reviews': commented_reviews,
        'user_form': user_form,
        'details_form': details_form,
        'is_google_user': profile_user.socialaccount_set.exists(),
        'is_current_user': True,
        'books_read': books_read,
        'books_want_to_read': books_want_to_read,
        "pma_flag": (
            request.user.groups.filter(name="PMA").exists()
            if request.user.is_authenticated
            else False
        ),
    }
    return render(request, 'users/profile.html', context)

def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)
    reviews_written = profile_user.book_reviews.all()
    commented_reviews = BookReview.objects.filter(comments__user=profile_user).distinct()

    is_current_user = request.user == profile_user  # viewing own profile check

    # get bookshelves
    books_read = profile_user.user_books.filter(status='read')
    books_want_to_read = profile_user.user_books.filter(status='want_to_read')

    if is_current_user:
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=profile_user)
            details_form = UserDetailsForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and details_form.is_valid():
                user_form.save()
                details_form.save()
                return redirect('view_profile', username=username)  # redirects to avoid resubmission
        else:
            user_form = UserUpdateForm(instance=profile_user)
            details_form = UserDetailsForm(instance=profile)
    else:
        # forms not needed when viewing someone else's profile
        user_form = None
        details_form = None

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'reviews_written': reviews_written,
        'commented_reviews': commented_reviews,
        'is_google_user': profile_user.socialaccount_set.exists(),
        'is_current_user': is_current_user,
        'books_read': books_read,
        'books_want_to_read': books_want_to_read,
        'user_form': user_form,
        'details_form': details_form,
        'pma_flag': (
            request.user.groups.filter(name="PMA").exists()
            if request.user.is_authenticated
            else False
        ),
    }
    return render(request, 'users/profile.html', context)