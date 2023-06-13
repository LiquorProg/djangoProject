from django.urls import path

from .views import *

urlpatterns = [
    path('', BlogHome.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', BlogCategory.as_view(), name='category'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('user/posts/', UserPostListView.as_view(), name='user_posts'),
    path('post/<slug:post_slug>/edit/', EditPostView.as_view(), name='edit_post'),
    path('post/<slug:post_slug>/delete/', DeletePostView.as_view(), name='delete_post'),
]
