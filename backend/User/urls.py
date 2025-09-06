from django.urls import path
from .views import JwtLoginView, TestView

urlpatterns = [
    path('jwtLogin', JwtLoginView.as_view(), name='jwt-login'),  # 登录接口
    path('test', TestView.as_view(), name='test'),  # 测试接口
]