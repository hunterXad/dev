from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    ProfileDetailView,
    FollowUserView,
    UnfollowUserView,
    register_page,
    login_page,
    profile_page
)

urlpatterns = [
    # ✅ التسجيل
    path('api/register/', RegisterView.as_view(), name='register'),

    # ✅ تسجيل الدخول (JWT)
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # ✅ تجديد التوكن
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ عرض الملف الشخصي لأي مستخدم
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_detail'),

    # ✅ متابعة مستخدم
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow_user'),

    # ✅ إلغاء المتابعة
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow_user'),
    
    path('', register_page, name='home'),
    path('login/', login_page, name='login'),
    path('profile/', profile_page, name='profile'),
]
