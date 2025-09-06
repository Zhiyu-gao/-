import hashlib
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    class Meta:
        model = User
        fields = '__all__'  # 返回所有字段

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """自定义登录序列化器（处理密码加密和用户验证）"""
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)  # 调用父类生成token

    def validate(self, attrs):
        # 前端传的用户名和密码
        username = attrs.get('username')
        password = attrs.get('password')

        # 密码MD5加密（与PPT一致）
        m = hashlib.md5()
        m.update(password.encode("utf-8"))
        encrypted_pwd = m.hexdigest()

        # 验证用户
        try:
            user = User.objects.get(username=username, password=encrypted_pwd)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('账号或密码错误')

        # 生成token
        refresh = self.get_token(user)
        return {
            'userId': user.id,
            'token': str(refresh.access_token),  # 访问令牌
            'refresh': str(refresh)  # 刷新令牌
        }