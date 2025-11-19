from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name = 'home'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)