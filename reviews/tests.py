from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from reviews.models import BookReview, BookReviewMembership, JoinRequest
from django.utils.timezone import now

class ReviewViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.login(username='testuser', password='testpassword')

        self.review1 = BookReview.objects.create(
            user=self.user,
            title="Sample Review 1",
            author="Author 1",
            genre="Fiction",
            comment="This is a test comment.",
            rating=5,
            date=now(),
        )
        self.review2 = BookReview.objects.create(
            user=self.other_user,
            title="Sample Review 2",
            author="Author 2",
            genre="Non-Fiction",
            comment="Another test comment.",
            rating=4,
            date=now(),
        )

    def test_review_list_view(self):
        response = self.client.get(reverse('review_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_review_view(self):
        response = self.client.get(reverse('create_review'))
        self.assertEqual(response.status_code, 200)

    def test_author_reviews_view(self):
        response = self.client.get(reverse('author_reviews', args=[self.review1.author]))
        self.assertEqual(response.status_code, 200)

    def test_genre_reviews_view(self):
        response = self.client.get(reverse('genre_reviews', args=['Fiction']))
        self.assertEqual(response.status_code, 200)

    def test_search_reviews_view(self):
        response = self.client.get(reverse('review_list'), {'search_query': 'Sample'})
        self.assertEqual(response.status_code, 200)

    def test_join_review_view(self):
        response = self.client.post(reverse('join_review', args=[self.review2.id]))
        self.assertEqual(response.status_code, 302)
        join_request = JoinRequest.objects.filter(user=self.user, review=self.review2).first()
        self.assertIsNotNone(join_request)

    def test_manage_join_requests_view_as_owner(self):
        self.client.logout()
        self.client.login(username='otheruser', password='password123')
        join_request = JoinRequest.objects.create(user=self.user, review=self.review2)
        response = self.client.post(reverse('manage_join_requests', args=[self.review2.id]), {
            'action': 'accept',
            'join_request_id': join_request.id
        })
        self.assertEqual(response.status_code, 302)
        join_request.refresh_from_db()
        self.assertEqual(join_request.status, JoinRequest.ACCEPTED)

    def test_leave_review_view(self):
        membership = BookReviewMembership.objects.create(user=self.user, review=self.review2)
        response = self.client.post(reverse('leave_review', args=[self.review2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BookReviewMembership.objects.filter(user=self.user, review=self.review2).exists())

    def test_review_detail_view_as_member(self):
        BookReviewMembership.objects.create(user=self.user, review=self.review2)
        response = self.client.get(reverse('review_detail', args=[self.review2.id]))
        self.assertEqual(response.status_code, 200)

    def test_remove_review_view(self):
        response = self.client.post(reverse('remove_book_review', args=[self.review1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BookReview.objects.filter(id=self.review1.id).exists())
