from rest_framework import serializers
from .models import Video, Category ,Stream

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['uploader']

class StreamSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Stream
        fields = ['id', 'title', 'youtube_id', 'status', 'category', 'category_name', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']