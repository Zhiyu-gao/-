from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User  # 导入自定义用户模型

class MyJWTAuthentication(JWTAuthentication):
    """自定义JWT认证，适配自有用户表"""
    def get_user(self, validated_token):
        try:
            user_id = validated_token["user_id"]  # 从token中获取用户ID
        except KeyError:
            raise AuthenticationFailed(_('Token格式错误'))

        try:
            user = User.objects.get(id=user_id)  # 从自定义用户表查询
        except User.DoesNotExist:
            raise AuthenticationFailed(_('用户不存在'))
        return user