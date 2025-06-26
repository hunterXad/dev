from rest_framework import serializers
from .models import CustomUser, Profile
from django.contrib.auth.password_validation import validate_password

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'profile_picture']
    
# ✅ 1. تسجيل مستخدم
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'bio']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data.get('bio', ''),
            password=validated_data['password']
        )
        # إنشاء بروفايل تلقائي
        
        return user


# ✅ 2. ملف المستخدم (البروفايل)
class ProfileSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    bio = serializers.CharField(source='user.bio', read_only=True)
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    score = serializers.IntegerField(read_only=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'user', 'bio', 'profile_picture', 'score',
            'following', 'followers',
            'following_count', 'followers_count'
        ]

    def get_following(self, obj):
        return UserMiniSerializer([p.user for p in obj.following.all()], many=True).data

    def get_followers(self, obj):
        followers_profiles = Profile.objects.filter(following=obj)
        return UserMiniSerializer([p.user for p in followers_profiles], many=True).data

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return Profile.objects.filter(following=obj).count()
