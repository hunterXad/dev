from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Profile
from .serializers import RegisterSerializer, ProfileSerializer, UserMiniSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

User = get_user_model()

# ✅ 1. تسجيل مستخدم جديد
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# ✅ 2. عرض الملف الشخصي
class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'
    permission_classes = [permissions.AllowAny]


# ✅ 3. متابعة مستخدم
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)

        if target_user == request.user:
            return Response({"detail": "❌ لا يمكنك متابعة نفسك!"}, status=status.HTTP_400_BAD_REQUEST)

        if target_user.profile in request.user.profile.following.all():
            return Response({"detail": f"⚠️ أنت بالفعل تتابع {username}"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.profile.following.add(target_user.profile)
        return Response({"detail": f"✅ تم متابعة {username}"})


# ✅ 4. إلغاء متابعة مستخدم
class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)

        if target_user == request.user:
            return Response({"detail": "❌ لا يمكنك إلغاء متابعة نفسك!"}, status=status.HTTP_400_BAD_REQUEST)

        if target_user.profile not in request.user.profile.following.all():
            return Response({"detail": f"⚠️ أنت لا تتابع {username} أصلاً"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.profile.following.remove(target_user.profile)
        return Response({"detail": f"✅ تم إلغاء متابعة {username}"})


# ✅ 5. قائمة من يتابعهم المستخدم
class FollowingListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        following_profiles = user.profile.following.all()
        following_users = [p.user for p in following_profiles]
        return Response(UserMiniSerializer(following_users, many=True).data)


# ✅ 6. قائمة من يتابعون المستخدم
class FollowersListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        followers_profiles = Profile.objects.filter(following=user.profile)
        followers_users = [p.user for p in followers_profiles]
        return Response(UserMiniSerializer(followers_users, many=True).data)


# ✅ صفحات HTML
def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def profile_page(request):
    return render(request, 'profile.html')
