from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from reviews.models import Comment, BookReview
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

class UserAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='regularuser', password='thisisnotasecurepassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword123')
        
        self.image_path = os.path.join(settings.BASE_DIR, 'imagesS3', 'images.jpg')
        
        with open(self.image_path, 'rb') as image_file:
            self.uploaded_file = SimpleUploadedFile(
                name='test_image.jpg',
                content=image_file.read(),
                content_type='image/jpeg'
            )
        
        self.review1 = BookReview.objects.create(
            user=self.user,
            title='Back to the Future 1',
            author='Robert Zemeckis',
            genre='SCI_FI',
            comment='Kinda Goated ngl.',
            rating=5,
            file_upload=self.uploaded_file
        )
        self.review2 = BookReview.objects.create(
            user=self.user,
            title='Back to the Future 2',
            author='Robert Zemeckis',
            genre='SCI_FI',
            comment='Goated',
            rating=5,
            file_upload=self.uploaded_file
        )
        self.review3 = BookReview.objects.create(
            user=self.user,
            title='Harry Potter and the Goblet of Fire',
            author='J.K. Rowling',
            genre='FICT',
            comment='Luh Calm Beerbow',
            rating=4,
            file_upload=self.uploaded_file
        )

    def test_regular_user_cannot_access_admin(self):
        self.client.login(username='regularuser', password='thisisnotasecurepassword')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_admin_user_can_access_admin(self):
        self.client.login(username='adminuser', password='adminpassword123')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_profile_access(self):
        self.client.login(username='regularuser', password='thisisnotasecurepassword')
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)

    def test_review_exists(self):
        self.client.login(username='regularuser', password='thisisnotasecurepassword')
        response = self.client.get(reverse('review_list'))
        self.assertEqual(response.status_code, 200)
        self.client.post(reverse('create_review'), {
            'title': 'Back to the Future 3',
            'author': 'Another Author',
            'genre': 'SCI_FI',
            'comment': 'Zest',
            'rating': 4,
        })
        self.assertTrue(BookReview.objects.filter(title='Back to the Future 3', author='Another Author').exists())

    def test_search_by_title(self):
        self.client.login(username='regularuser', password='thisisnotasecurepassword')
        search_term = 'Back to the Future'
        response = self.client.get(reverse('search_results'), {'search_query': search_term})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Back to the Future 1')
        self.assertContains(response, 'Back to the Future 2')
        self.assertNotContains(response, 'Harry Potter and the Goblet of Fire')

    def test_search_by_genre(self):
        self.client.login(username='regularuser', password='thisisnotasecurepassword')
        search_term = 'SCI_FI'
        response = self.client.get(reverse('search_results'), {'search_query': search_term})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Back to the Future 1')
        self.assertContains(response, 'Back to the Future 2')
        self.assertNotContains(response, 'Harry Potter and the Goblet of Fire')

    def test_search_by_author(self):
        self.client.login(username='regularuser', password='thisisnotasecurepassword')
        search_term = 'Robert Zemeckis'
        response = self.client.get(reverse('search_results'), {'search_query': search_term})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Back to the Future 1')
        self.assertContains(response, 'Back to the Future 2')
        self.assertNotContains(response, 'Harry Potter and the Goblet of Fire')

    def test_non_logged_in_user_sees_title_only(self):
        response = self.client.get(reverse('review_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review1.title)
        self.assertNotContains(response, self.review1.file_upload.url)
 
    def test_user_profile(self):
        self.client.login(username='regularuser', password='thisisnotasecurepassword')
        response = self.client.get(reverse('view_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review1.title)
        self.assertContains(response, self.review2.title)
        self.assertContains(response, self.review3.title)
    def test_other_user_can_view_user_profile(self):
        other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.login(username='otheruser', password='password123')
        response = self.client.get(reverse('view_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review1.title)
        self.assertContains(response, self.review2.title)
        self.assertContains(response, self.review3.title)
    def user_signin_tojoinreview(self):
        self.client.login(username='regularuser', password='thisisnotasecurepassword')
        response = self.client.post(reverse('join_review', args=[self.review1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BookReview.objects.filter(title='Back to the Future 1', author='Robert Zemeckis').exists())
    def user_nonsignin_noreview(self):
        response = self.client.post(reverse('join_review', args=[self.review1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BookReview.objects.filter(title='Back to the Future 1', author='Robert Zemeckis').exists()) 
 