from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('signup', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('user-profile/<str:pk>', views.profilePage, name='user-profile'),
    path('logout', views.logoutPage, name='logout'),
    path('post-feed', views.post, name='post-feed'),
    path('post-detail/<str:pk>', views.post_detail, name='post-detail'),
    path('like-post', views.likePost, name='like-post'),
    path('follow', views.follow, name='follow'),
    path('follow-page', views.medium_follow, name='follow-page'),
    path('suggestion-page', views.medium_suggestion, name='suggestion-page'),
    path('edit-feed/<str:pk>', views.update_post, name='edit-feed'),
    path('delete-feed/<str:pk>', views.delete_post, name='delete-feed')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)