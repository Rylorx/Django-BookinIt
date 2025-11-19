import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BookReview, BookReviewMembership, Comment, JoinRequest
from .forms import BookReviewForm, BookSearchForm, CommentForm, ReviewForm
from django.http import JsonResponse
from django.db.models import Q, Avg
import logging
from django.contrib import messages
from django.urls import reverse
from books.models import Book
from django.utils import timezone

logger = logging.getLogger(__name__)


def about(request):
    context  = { "pma_flag": (
            request.user.groups.filter(name="PMA").exists()
            if request.user.is_authenticated
            else False
        ),}
    return render(request, "reviews/about.html", context)


@login_required
def create_review(request, book_id=None):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()

            membership, created = BookReviewMembership.objects.get_or_create(
                review=review, 
                user=request.user,
            )

            return redirect("home")  # Adjust the redirect as needed
    else:
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            form = ReviewForm(
                initial={
                    "title": book.title,
                    "author": book.author,
                    "genre": book.genre,
                }
            )
        else:
            form = ReviewForm()

    context = {"form": form,
               
               "pma_flag": (
                request.user.groups.filter(name="PMA").exists()
                if request.user.is_authenticated
                else False
                ),
               
               }
    return render(request, "reviews/create_review.html", context)

@login_required
def leave_review(request, review_id):
    review = get_object_or_404(BookReview, id=review_id)
    if request.user == review.user:
        messages.error(request, "You cannot leave your own review.")
        return redirect('home')
        
    membership = get_object_or_404(BookReviewMembership, user=request.user, review=review)
    membership.delete()
    messages.success(request, f"You have left the review for {review.title}")
    return redirect('home')

def review_list(request):
    reviews = BookReview.objects.all()

    sort_by = request.GET.get("sort_by", "")
    sort_direction = request.GET.get("sort_direction", "desc")

    order_prefix = "-" if sort_direction == "desc" else ""

    if sort_by:
        if sort_by == "rating":
            reviews = reviews.order_by(f"{order_prefix}rating")
        elif sort_by == "date":
            reviews = reviews.order_by(f"{order_prefix}date")
        elif sort_by == "author":
            reviews = reviews.order_by(f"{order_prefix}author")
        elif sort_by == "title":
            reviews = reviews.order_by(f"{order_prefix}title")
    else:
        # Default sorting if no sort parameter is provided
        reviews = reviews.order_by("-date")

    if request.user.is_authenticated:
        membership_ids = set(
            request.user.memberships.values_list("review_id", flat=True)
        )
    else:
        membership_ids = set()

    context = {
        "reviews": reviews,
        "membership_ids": membership_ids,
        "pma_flag": (
            request.user.groups.filter(name="PMA").exists()
            if request.user.is_authenticated
            else False
        ),
    }

    return render(request, "reviews/review_list.html", context)


def author_reviews(request, author):
    reviews = BookReview.objects.filter(author=author)
    return render(
        request,
        "reviews/author_reviews.html",
        {
            "author": author,
            "reviews": reviews,
            "pma_flag": (
            request.user.groups.filter(name="PMA").exists()
            if request.user.is_authenticated
            else False
            ),


        },
    )


def genre_reviews(request, genre):
    reviews = BookReview.objects.filter(genre=genre)
    return render(
        request, "reviews/genre_reviews.html", {"genre": genre, "reviews": reviews, "pma_flag": (
            request.user.groups.filter(name="PMA").exists()
            if request.user.is_authenticated
            else False),}
    )


@login_required
def remove_book_review(request, review_id):
    review = get_object_or_404(BookReview, id=review_id)
    if request.user == review.user or request.user.groups.filter(name="PMA").exists():
        review.delete()
        messages.success(request, f"Review for {review.title} deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this review.")
    return redirect("review_list")


def book_list(request):
    form = BookSearchForm(request.GET)
    reviews = BookReview.objects.all()

    logger.debug(f"Form data: {request.GET}")
    logger.debug(f"Form is bound: {form.is_bound}")

    if form.is_valid():
        logger.info("Form is valid")
        search_query = form.cleaned_data.get("search_query")
        logger.info(f"Search query: {search_query}")
        if search_query:
            reviews = reviews.filter(
                Q(title__icontains=search_query)
                | Q(author__icontains=search_query)
                | Q(genre__icontains=search_query)
                | Q(file_title__icontains=search_query)
                | Q(file_keywords__icontains=search_query)
            )
            logger.info(f"Filtered reviews count: {reviews.count()}")
    else:
        logger.warning(f"Form errors: {form.errors}")

    context = {
        "form": form,
        "reviews": reviews,
        "pma_flag": (
            request.user.groups.filter(name="PMA").exists()
            if request.user.is_authenticated
            else False
        ),
    }
    return render(request, "reviews/search_results.html", context)

@login_required
def join_review(request, review_id):
    if request.method == "POST" and request.user.is_authenticated:
        review = get_object_or_404(BookReview, id=review_id)
        
        # Check if user is review owner
        if review.user == request.user:
            messages.error(request, "You cannot join your own review - you're already a member.")
            return redirect("review_list")

        # Check if user is PMA
        if request.user.groups.filter(name="PMA").exists():
            # Direct join for PMA users
            membership, created = BookReviewMembership.objects.get_or_create(
                review=review, 
                user=request.user
            )

            if created:
                messages.success(request, f"You have joined the review for {review.title}")
            else:
                messages.info(request, f"You are already a member of the review for {review.title}")
        else:
            # Create join request for regular users
            join_request, created = JoinRequest.objects.get_or_create(
                review=review,
                user=request.user
            )
            if created:
                messages.success(request, f"Your request to join the review for {review.title} has been sent")
            else:
                messages.info(request, f"You have already requested to join this review")

        return redirect("review_list")

    return redirect("home")

from django.db.models import Avg, Count


@login_required
def review_detail(request, review_id):
    review = get_object_or_404(BookReview, id=review_id)
    comments = review.comments.all()
    join_requests = JoinRequest.objects.filter(review=review, status=JoinRequest.PENDING)
    membership = BookReviewMembership.objects.filter(user=request.user, review=review).first()

    if request.method == "POST":
        if 'leave_review' in request.POST:
            if membership:
                membership.leave_review()
            return redirect("review_detail", review_id=review_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()

            comment_ratings = review.comments.aggregate(Avg("rating"), Count("rating"))
            total_ratings = (
                comment_ratings["rating__avg"] * comment_ratings["rating__count"]
                if comment_ratings["rating__avg"]
                else 0
            )

            total_ratings += review.rating
            total_count = comment_ratings["rating__count"] + 1
            new_average_rating = total_ratings / total_count if total_count else 0

            review.rating = round(new_average_rating, 2)
            review.save()

            return redirect("review_detail", review_id=review_id)
    else:
        form = CommentForm()

    context = {
        "review": review,
        "comments": comments,
        "form": form,
        "join_requests": join_requests,
        "membership": membership,
        "pma_flag": (
            request.user.groups.filter(name="PMA").exists()
            if request.user.is_authenticated
            else False
        ),
    }
    return render(request, "reviews/review_detail.html", context)

@login_required
def join_review_request(request, review_id):
    if request.method == "POST":
        review = get_object_or_404(BookReview, id=review_id)
        
        # This makes sure that the user is NOT allowed to request to join their own review
        if review.user == request.user:
            messages.error(request, "You cannot request to join your own review.")
            return redirect("review_list")
        
        join_request, created = JoinRequest.objects.get_or_create(
            review=review, user=request.user
        )

        if created:
            messages.success(request, f"Your request to join this review has been sent.")
        else:
            messages.info(request, f"You have already requested to join this review.")
        
        return redirect("review_list")
    return redirect("home")

@login_required
def manage_join_requests(request, review_id):
    
    review = get_object_or_404(BookReview, id=review_id)

    if review.user != request.user and not request.user.groups.filter(name="PMA").exists():
        messages.error(request, "You are not authorized to manage requests for this review.")
        return redirect("review_list")

    # requests = JoinRequest.objects.filter(review=review, status=JoinRequest.PENDING)

    if request.method == "POST" and request.user.is_authenticated:
        action = request.POST.get("action")
        join_request_id = request.POST.get("join_request_id")
        
        logger.info(f"Action: {action}, Join Request ID: {join_request_id}")
        join_request = get_object_or_404(JoinRequest, id=join_request_id)


        if action == "accept":
            join_request.status = JoinRequest.ACCEPTED
            join_request.save()
            logger.info(f"Accepted request from {join_request.user.username}")


            membership, created = BookReviewMembership.objects.get_or_create(user=join_request.user, review=review)

            if created:
                logger.info(f"Created membership for {join_request.user.username}")
            messages.success(request, f"Request from {join_request.user.username} has been accepted.")
            # logger.info(f"Request from {join_request.user.username} has been accepted.")
        elif action == "reject":
            join_request.status = JoinRequest.REJECTED
            join_request.save()
            logger.info(f"Rejected request from {join_request.user.username}")
            messages.info(request, f"Request from {join_request.user.username}'s request has been rejected.")



    join_requests = JoinRequest.objects.filter(review=review, status=JoinRequest.PENDING)
    # return render(request, "reviews/manage_join_requests.html", {"review": review, "requests": join_requests})
    return redirect("review_detail", review_id=review_id)
