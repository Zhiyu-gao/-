from django.shortcuts import render

# DRF 基础导入
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

# 业务模型与序列化
from .models import Well
from .serializers import WellSerializer

# 系统与图片处理
import os
from django.conf import settings
from PIL import Image

import torch
from torchvision import models, transforms
from PIL import Image
import os

# 加载模型（只加载一次）
MODEL_PATH = os.path.join('d:/aaaaaaaaaaaaaaaaaaaaaa/manhole_cover/models', 'finetune_resnet18.pth')
NUM_CLASSES = 5  # 修改为你的类别数

model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, NUM_CLASSES)
model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def predict_image(image_path):
    img = Image.open(image_path).convert('RGB')
    input_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        pred = output.argmax(dim=1).item()
    return f"[{pred}]"

# 井盖信息分页查询接口
class WellAPIView(APIView):
    permission_classes = [AllowAny]
    """井盖信息接口（支持分页查询）"""
    def get(self, request):
        page = int(request.GET.get('page', 1))  # 页码
        page_size = 10  # 每页10条
        start = (page - 1) * page_size
        end = start + page_size

        # 查询数据并分页
        well_list = Well.objects.all()[start:end]
        total = Well.objects.count()  # 总条数

        return Response({
            "wellData": WellSerializer(well_list, many=True).data,
            "total": total
        })

# 井盖图片上传与自动检测接口
class FileUploadView(APIView):
    """文件上传接口（处理井盖图片上传）"""
    permission_classes = [AllowAny]
    def post(self, request):
        # 获取上传的文件
        file = request.FILES.get('upload_file')
        if not file:
            return Response({"error": "未上传文件"}, status=400)

        # 保存文件到 static 目录
        file_path = os.path.join(settings.STATIC_ROOT, file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # 调用模型进行预测（你可以替换为真实模型推理代码）
        predicted_category = predict_image(file_path)

        return Response({
            "path": f"/static/{file.name}",  # 图片路径
            "label": predicted_category      # 预测结果
        })

# 井盖图片检测模型推理函数（需替换为你的真实模型代码）

# 井盖标注信息更新接口
class UpdateAnnotationView(APIView):
    permission_classes = [AllowAny]
    def put(self, request):
        try:
            well_id = request.data.get('id')
            well = Well.objects.get(id=well_id)
            serializer = WellSerializer(well, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Well.DoesNotExist:
            return Response({"error": "数据不存在"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.viewsets import ModelViewSet
from .models import Monitor
from .serializers import MonitorSerializer

class MonitorViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer