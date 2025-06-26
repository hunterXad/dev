from .models import Video, Category ,Stream , Playlist, PlaylistItem
from rest_framework import viewsets, permissions, filters ,generics
from .serializers import VideoSerializer, CategorySerializer , StreamSerializer , PlaylistSerializer, PlaylistItemSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StreamForm , StreamStatusForm
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from .models import Playlist
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-uploaded_at')
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



# عرض كل البثوث
def stream_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    streams = Stream.objects.all()

    if search_query:
        streams = streams.filter(title__icontains=search_query)

    if category_filter:
        streams = streams.filter(category_id=category_filter)

    streams = streams.order_by('-created_at')
    categories = Category.objects.all()

    return render(request, 'stream_list.html', {
        'streams': streams,
        'categories': categories,
    })

# إنشاء بث جديد
def create_stream(request):
    if request.method == 'POST':
        form = StreamForm(request.POST)
        if form.is_valid():
            stream = form.save(commit=False)
            stream.owner = request.user
            stream.save()
            return redirect('stream_list')
    else:
        form = StreamForm()
    return render(request, 'create_stream.html', {'form': form})


def watch_stream(request, stream_id):
    stream = get_object_or_404(Stream, id=stream_id)
    can_edit = request.user == stream.owner

    if request.method == 'POST' and can_edit:
        form = StreamStatusForm(request.POST, instance=stream)
        if form.is_valid():
            form.save()
            return redirect('watch_stream', stream_id=stream.id)
    else:
        form = StreamStatusForm(instance=stream)

    return render(request, 'watch_stream.html', {
        'stream': stream,
        'form': form,
        'can_edit': can_edit
    })
    
    
class StreamListCreateAPI(generics.ListCreateAPIView):
    queryset = Stream.objects.all().order_by('-created_at')
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'youtube_id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# عرض أو تعديل أو حذف بث واحد
class StreamRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # تأكد أن المستخدم هو صاحب البث
        if self.request.user != self.get_object().owner:
            raise PermissionDenied("❌ غير مسموح لك تعديل هذا البث")
        serializer.save()
        
        


class PlaylistListCreateView(generics.ListCreateAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AddItemToPlaylistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
        video_id = request.data.get("video_id")
        stream_id = request.data.get("stream_id")

        if not video_id and not stream_id:
            return Response({"detail": "يجب تحديد video_id أو stream_id"}, status=400)

        if video_id and stream_id:
            return Response({"detail": "لا يمكن تحديد فيديو وبث في نفس الوقت"}, status=400)

        if video_id:
            video = get_object_or_404(Video, id=video_id)
            item = PlaylistItem.objects.create(playlist=playlist, video=video)
        else:
            stream = get_object_or_404(Stream, id=stream_id)
            item = PlaylistItem.objects.create(playlist=playlist, stream=stream)

        return Response(PlaylistItemSerializer(item).data, status=201)


class DeleteItemFromPlaylistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        item = get_object_or_404(PlaylistItem, id=item_id, playlist__owner=request.user)
        item.delete()
        return Response({"detail": "تم الحذف"}, status=204)


User = get_user_model()

class UserPublicPlaylistsView(TemplateView):
    template_name = "public_playlists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        user = User.objects.get(username=username)
        context["owner"] = user
        context["playlists"] = Playlist.objects.filter(owner=user)
        return context
    
    
def playlist_detail_view(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    return render(request, "playlist_detail.html", {"playlist": playlist})

class PlaylistUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # فقط المستخدم يقدر يعدل/يحذف قوائمه
        return Playlist.objects.filter(owner=self.request.user)

def my_playlists_view(request):
    return render(request, "my_playlists.html")



class AllVideosView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class AllStreamsView(ListAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer