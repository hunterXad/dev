from rest_framework import serializers
from .models import CustomUser, Profile
from django.contrib.auth.password_validation import validate_password


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
    user = serializers.StringRelatedField(read_only=True)
    bio = serializers.CharField(source='user.bio', read_only=True)
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    following = serializers.SlugRelatedField(many=True, read_only=True, slug_field='user__username')
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture', 'score', 'following', 'followers']

    def get_followers(self, obj):
        return [profile.user.username for profile in Profile.objects.filter(following=obj)]
