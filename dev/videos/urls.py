from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    VideoViewSet, CategoryViewSet,
    StreamListCreateAPI, StreamRetrieveUpdateDestroyAPI,
    stream_list, create_stream, watch_stream
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

    # ✅ صفحات HTML (غير مهمة للـ frontend ولكن احتفظنا بها لو احتجتها لاحقًا)
    path('', stream_list, name='stream_list'),
    path('create/', create_stream, name='create_stream'),
    path('watch/<int:stream_id>/', watch_stream, name='watch_stream'),
]
