import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# 预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 加载预训练模型
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 2)  # 假设你有2类，改成你的类别数

# 只训练最后一层
for param in model.parameters():
    param.requires_grad = False
for param in model.fc.parameters():
    param.requires_grad = True

# 构造训练数据
def load_img(path):
    img = Image.open(path).convert('RGB')
    return transform(img)

train_image_paths = [...]  # 你的训练图片路径列表
train_labels = [...]       # 你的训练标签列表（如0/1）

inputs = torch.stack([load_img(p) for p in train_image_paths])
labels = torch.tensor(train_labels)

# 训练最后一层
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()
model.train()
for epoch in range(20):  # 轮数可调
    outputs = model(inputs)
    loss = criterion(outputs, labels)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# 保存模型
torch.save(model.state_dict(), "finetune_resnet18.pth")