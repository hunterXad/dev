from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Profile
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated

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
    lookup_url_kwarg = 'username'  # ✅ حل المشكلة
    permission_classes = [permissions.AllowAny]
    
# ✅ 3. متابعة مستخدم
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)
        if target_user == request.user:
            return Response({"detail": "❌ لا يمكنك متابعة نفسك!"}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.profile.following.add(target_user.profile)
        return Response({"detail": f"✅ تم متابعة {username}"})

# ✅ 4. إلغاء متابعة مستخدم
class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)
        if target_user == request.user:
            return Response({"detail": "❌ لا يمكنك إلغاء متابعة نفسك!"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.profile.following.remove(target_user.profile)
        return Response({"detail": f"✅ تم إلغاء متابعة {username}"})


from django.shortcuts import render

def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def profile_page(request):
    return render(request, 'profile.html')