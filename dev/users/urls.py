from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    ProfileDetailView,
    FollowUserView,
    UnfollowUserView,
    FollowersListView,     # ✅ أضف هذا
    FollowingListView,     # ✅ وأضف هذا
    register_page,
    login_page,
    profile_page
)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<str:username>/following/', FollowingListView.as_view(), name='following_list'),  # ✅
    path('profile/<str:username>/followers/', FollowersListView.as_view(), name='followers_list'),  # ✅

    path('follow/<str:username>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow_user'),

    path('', register_page, name='home'),
    path('login/', login_page, name='login'),
    path('profile/', profile_page, name='profile'),
]
