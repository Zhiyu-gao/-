from rest_framework import serializers
from.models import Well

class WellSerializer(serializers.ModelSerializer):
    wellurl = serializers.SerializerMethodField()

    class Meta:
        model = Well
        fields = ('id', 'wellurl', 'bbox', 'user', 'category', 'image_id')

    def get_wellurl(self, obj):
        if obj.image_id:
            # 假设图片存储在 media/images 目录下，根据实际情况修改路径
            return f"/static/{obj.image_id}.jpg"
        return ""
    
from rest_framework import serializers
from .models import Monitor

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = "__all__"  # 可根据实际需求指定具体字段，如 ['id', 'time', 'position', ...]