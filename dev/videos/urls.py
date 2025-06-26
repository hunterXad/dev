from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    VideoViewSet, CategoryViewSet,
    StreamListCreateAPI, StreamRetrieveUpdateDestroyAPI,
    stream_list, create_stream, watch_stream ,PlaylistListCreateView,
    AddItemToPlaylistView,
    DeleteItemFromPlaylistView,
    UserPublicPlaylistsView,
    playlist_detail_view,
    my_playlists_view,AllVideosView,AllStreamsView,PlaylistUpdateDeleteView
)

# Router للـ ViewSets الخاصة بالفيديو والتصنيفات
router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='videos')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    # ✅ API URLs للفيديوهات والتصنيفات والبثوث
    path('api/', include(router.urls)),

    # ✅ API endpoints للبثوث (Create/List + Retrieve/Update/Delete)
    path('api/streams/', StreamListCreateAPI.as_view(), name='api_stream_list_create'),
    path('api/streams/<int:pk>/', StreamRetrieveUpdateDestroyAPI.as_view(), name='api_stream_detail'),

    
     # ✅ عرض وإنشاء قوائم التشغيل
    path('api/playlists/', PlaylistListCreateView.as_view(), name='playlist-list-create'),

    # ✅ إضافة عنصر (فيديو أو بث) لقائمة تشغيل
    path('api/playlists/<int:playlist_id>/add/', AddItemToPlaylistView.as_view(), name='playlist-add-item'),

    # ✅ حذف عنصر من قائمة تشغيل
    path('api/playlist-items/<int:item_id>/delete/', DeleteItemFromPlaylistView.as_view(), name='playlist-delete-item'),
    path('api/playlists/<int:pk>/', PlaylistUpdateDeleteView.as_view(), name='playlist-edit-delete'),
    
    path('users/<str:username>/playlists/', UserPublicPlaylistsView.as_view(), name='user-public-playlists'),
    path('playlist/<int:playlist_id>/', playlist_detail_view, name='playlist-detail'),
    path('my-playlists/', my_playlists_view, name='my-playlists'),
    # ✅ صفحات HTML (غير مهمة للـ frontend ولكن احتفظنا بها لو احتجتها لاحقًا)
    path('', stream_list, name='stream_list'),
    path('create/', create_stream, name='create_stream'),
    path('watch/<int:stream_id>/', watch_stream, name='watch_stream'),
    path('api/videos/', AllVideosView.as_view(), name='all-videos'),
    path('api/streams/', AllStreamsView.as_view(), name='all-streams'),
]
