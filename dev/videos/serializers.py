from rest_framework import serializers
from .models import Video, Category ,Stream , PlaylistItem , Playlist

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
        
        
        
class PlaylistItemSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    stream = StreamSerializer(read_only=True)

    class Meta:
        model = PlaylistItem
        fields = ['id', 'video', 'stream', 'added_at']


class PlaylistSerializer(serializers.ModelSerializer):
    items = PlaylistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'description', 'created_at', 'items']