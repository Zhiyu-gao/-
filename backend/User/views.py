from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MyTokenObtainPairSerializer, UserSerializer

class JwtLoginView(APIView):
    """登录视图（无需认证）"""
    authentication_classes = ()  # 关闭认证
    permission_classes = ()     # 关闭权限校验

    def post(self, request):
        # 调用自定义序列化器验证并生成token
        serializer = MyTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class TestView(APIView):
    """测试视图（需登录）"""
    def get(self, request):
        # 返回当前登录用户信息
        return Response({
            "user_info": UserSerializer(request.user).data
        })