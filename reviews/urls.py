from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import join_review
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('create/', views.create_review, name='create_review'),
    path('create_review/<int:book_id>/', views.create_review, name='create_review_with_book'),
    path('author/<str:author>/', views.author_reviews, name='author_reviews'),
    path('genre/<str:genre>/', views.genre_reviews, name='genre_reviews'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', views.book_list, name='search_results'),
    path('join/<int:review_id>/', join_review, name='join_review'),
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),
    path('about/', views.about, name='about'),
    path('remove_book_review/<int:review_id>/', views.remove_book_review, name='remove_book_review'),
    path('reviews/<int:review_id>/join-request/', views.join_review_request, name='join_review_request'),
    path('reviews/<int:review_id>/manage-requests/', views.manage_join_requests, name='manage_join_requests'),
    path('review/<int:review_id>/leave/', views.leave_review, name='leave_review'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)