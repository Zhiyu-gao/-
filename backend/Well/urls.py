from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'monitor', MonitorViewSet)

urlpatterns = [
    path('wellApi', WellAPIView.as_view(), name='well-api'),  # 井盖信息接口
    path('upload', FileUploadView.as_view(), name='file-upload'),  # 文件上传接口
    path('updateAnnotation', UpdateAnnotationView.as_view(), name='update-annotation'),
    path('', include(router.urls)),
]