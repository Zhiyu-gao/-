<template>
  <div class="container">
    <!-- 左侧导航轴 -->
    <div class="left-sidebar">
      <div class="steps-axis">
        <!-- 连接线 -->
        <div class="axis-line" :style="{ height: axisLineHeight }"></div>
        
        <!-- 步骤点 -->
        <div class="step-item" :class="{ active: currentStep === 1 }" @click="goToStep(1)">
          <div class="step-dot"></div>
          <div class="step-label">隐患类型</div>
        </div>
        
        <div class="step-item" :class="{ active: currentStep === 2 }" @click="goToStep(2)">
          <div class="step-dot"></div>
          <div class="step-label">bbox标注</div>
        </div>
        
        <div class="step-item" :class="{ active: currentStep === 3 }" @click="goToStep(3)">
          <div class="step-dot"></div>
          <div class="step-label">提交</div>
        </div>
      </div>
    </div>
    
    <!-- 右侧内容区域 -->
    <div class="right-content">
      <!-- 标题 -->
      <h1 class="page-title">训练数据管理</h1>
      
      <!-- 内容区域根据当前步骤显示不同内容 -->
      <div class="content-wrapper">
        <!-- 步骤1：隐患类型 -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="content-header">
            <h2>隐患类型选择</h2>
            <p>请选择图片中的井盖隐患类型</p>
          </div>
          
          <div class="content-body">
            <div class="image-container">
              <img 
                :src="selectedImageUrl" 
                alt="井盖图片" 
                class="well-image"
                v-if="selectedImageUrl"
              >
              <div class="placeholder" v-else>
                请从表格中选择一条数据
              </div>
            </div>
            
            <div class="options-container">
              <h3>选择隐患类型：</h3>
              <el-radio-group v-model="selectedCategory" class="category-radios">
                <el-radio :label="'[0]'">井盖完好</el-radio>
                <el-radio :label="'[1]'">井盖破损</el-radio>
                <el-radio :label="'[2]'">井盖缺失</el-radio>
                <el-radio :label="'[3]'">井盖未盖</el-radio>
                <el-radio :label="'[4]'">井圈问题</el-radio>
              </el-radio-group>
              
              <el-button 
                type="primary" 
                class="next-btn"
                @click="goToStep(2)"
                :disabled="!selectedImageUrl"
              >
                下一步：标注边界框
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- 步骤2：bbox标注 -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="content-header">
            <h2>边界框标注</h2>
            <p>请在图片上标注井盖位置</p>
          </div>
          
          <div class="content-body">
            <div class="image-container">
              <div class="annotation-container" v-if="selectedImageUrl">
                <img 
                  :src="selectedImageUrl" 
                  alt="井盖图片" 
                  class="well-image"
                  ref="annotationImage"
                  @mousedown="startDrawing"
                  @mousemove="drawBbox"
                  @mouseup="stopDrawing"
                  @mouseleave="stopDrawing"
                >
                <!-- 边界框 -->
                <div 
                  class="bbox"
                  v-if="bboxCoordinates"
                  :style="{
                    left: bboxCoordinates.x1 + 'px',
                    top: bboxCoordinates.y1 + 'px',
                    width: bboxCoordinates.width + 'px',
                    height: bboxCoordinates.height + 'px'
                  }"
                ></div>
              </div>
              <div class="placeholder" v-else>
                请从表格中选择一条数据
              </div>
            </div>
            
            <div class="bbox-info">
              <h3>边界框信息：</h3>
              <el-form :model="bboxForm" class="bbox-form">
                <el-form-item label="X1：">
                  <el-input v-model.number="bboxForm.x1" disabled></el-input>
                </el-form-item>
                <el-form-item label="Y1：">
                  <el-input v-model.number="bboxForm.y1" disabled></el-input>
                </el-form-item>
                <el-form-item label="X2：">
                  <el-input v-model.number="bboxForm.x2" disabled></el-input>
                </el-form-item>
                <el-form-item label="Y2：">
                  <el-input v-model.number="bboxForm.y2" disabled></el-input>
                </el-form-item>
              </el-form>
              
              <div class="btn-group">
                <el-button 
                  type="default" 
                  @click="goToStep(1)"
                >
                  上一步
                </el-button>
                <el-button 
                  type="primary" 
                  @click="goToStep(3)"
                  :disabled="!bboxCoordinates"
                >
                  下一步：提交
                </el-button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 步骤3：提交 -->
        <div v-if="currentStep === 3" class="step-content">
          <div class="content-header">
            <h2>提交标注信息</h2>
            <p>确认并提交标注信息</p>
          </div>
          
          <div class="content-body">
            <div class="summary-card">
              <h3>标注信息汇总</h3>
              
              <div class="summary-item">
                <span class="label">图片：</span>
                <img 
                  :src="selectedImageUrl" 
                  alt="井盖图片缩略图" 
                  class="thumbnail"
                  v-if="selectedImageUrl"
                >
              </div>
              
              <div class="summary-item">
                <span class="label">隐患类型：</span>
                <el-tag 
                  :type="getCategoryTagType(selectedCategory)"
                  class="category-tag"
                >
                  {{ getCategoryText(selectedCategory) }}
                </el-tag>
              </div>
              
              <div class="summary-item">
                <span class="label">边界框：</span>
                <span class="value">{{ bboxForm.x1 }}, {{ bboxForm.y1 }}, {{ bboxForm.x2 }}, {{ bboxForm.y2 }}</span>
              </div>
              
              <div class="btn-group">
                <el-button 
                  type="default" 
                  @click="goToStep(2)"
                >
                  上一步
                </el-button>
                <el-button 
                  type="primary" 
                  @click="submitAnnotation"
                  :loading="isSubmitting"
                >
                  确认提交
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 数据表格 -->
      <div class="table-container">
        <el-table 
          :data="tableData" 
          stripe 
          style="width: 100%;"
          @row-click="handleRowClick"
          :row-class-name="tableRowClassName"
        >
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column label="图像" width="150">
            <template #default="scope">
              <img :src="scope.row.wellurl" style="height: 50px;" />
            </template>
          </el-table-column>
          <el-table-column prop="bbox" label="边界框"></el-table-column>
          <el-table-column prop="category" label="分类"></el-table-column>
          <el-table-column label="状态">
            <template #default="scope">
              <el-tag v-if="scope.row.category === '[0]'">井盖完好</el-tag>
              <el-tag type="warning" v-if="scope.row.category === '[1]'">井盖破损</el-tag>
              <el-tag type="danger" v-if="scope.row.category === '[2]'">井盖缺失</el-tag>
              <el-tag type="danger" v-if="scope.row.category === '[3]'">井盖未盖</el-tag>
              <el-tag type="warning" v-if="scope.row.category === '[4]'">井圈问题</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed ,onMounted, inject } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router';

const tableData = ref([]); 

// 步骤导航相关
const currentStep = ref(1)
const axisLineHeight = computed(() => '200px')

// 图片和标注相关
const selectedImageUrl = ref('')
const selectedCategory = ref('')
const selectedRow = ref(null)
const router = useRouter();
const bboxCoordinates = ref(null)
const isDrawing = ref(false)
const startPoint = ref(null)
const annotationImage = ref(null)
const isSubmitting = ref(false)
const axios = inject('axios');  // 关键：使用提供的 api 实例

// 边界框表单数据
const bboxForm = ref({
  x1: 0,
  y1: 0,
  x2: 0,
  y2: 0
})

onMounted(async () => {
  try {
    // 3.1 获取登录时保存的 token（关键：通过认证）
    const token = sessionStorage.getItem('token');
    if (!token) {
      router.push('/login'); // 未登录则跳转登录页
      ElMessage.warning('请先登录');
      return;
    }

    // 3.2 发送请求到后端接口，携带 token
    const response = await axios.get('/well/wellApi', {
      headers: {
        'Authorization': `Bearer ${token}` // 携带认证信息
      }
    });

    // 3.3 关键：将后端返回的数据赋值给 tableData
    // 注意：这里的结构要和后端返回一致！
    // 例如：如果后端返回 { "data": [...] }，则改为 tableData.value = response.data.data;
    tableData.value = response.data.wellData; 

    // 打印数据到控制台，确认是否获取成功
    console.log('从后端获取的表格数据：', tableData.value);

  } catch (error) {
    console.error('获取数据失败：', error);
    // 错误处理：token 无效或接口错误
    if (error.response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录');
      sessionStorage.removeItem('token'); // 清除无效 token
      router.push('/login');
    } else {
      ElMessage.error('加载表格数据失败，请重试');
    }
  }
});


// 切换步骤
const goToStep = (step) => {
  currentStep.value = step
}

// 表格行点击事件
const handleRowClick = (row) => {
  // 直接将 row 赋值给 selectedRow.value
  selectedRow.value = row
  selectedImageUrl.value = row.wellurl

  // 如果有边界框数据，加载它
  if (row.bbox) {
    const [x1, y1, x2, y2] = row.bbox.split(',').map(Number)
    bboxCoordinates.value = { x1, y1, width: x2 - x1, height: y2 - y1 }
    bboxForm.value = { x1, y1, x2, y2 }
  } else {
    bboxCoordinates.value = null
    bboxForm.value = { x1: 0, y1: 0, x2: 0, y2: 0 }
  }

  // 如果有分类数据，加载它
  if (row.category) {
    selectedCategory.value = row.category
  } else {
    selectedCategory.value = ''
  }

  // 重置到第一步
  currentStep.value = 1
}

// 表格行样式
const tableRowClassName = ({ row }) => {
  return row === selectedRow.value? 'selected-row' : ''
}

// 边界框绘制相关方法
const startDrawing = (e) => {
  if (!annotationImage.value) return;
  const imgRect = annotationImage.value.getBoundingClientRect();
  startPoint.value = {
    x: e.clientX - imgRect.left,
    y: e.clientY - imgRect.top
  };
  isDrawing.value = true;
};

const drawBbox = (e) => {
  if (!isDrawing.value || !startPoint.value || !annotationImage.value) return;
  const imgRect = annotationImage.value.getBoundingClientRect();
  const currentX = e.clientX - imgRect.left;
  const currentY = e.clientY - imgRect.top;

  const x1 = Math.min(startPoint.value.x, currentX);
  const y1 = Math.min(startPoint.value.y, currentY);
  const x2 = Math.max(startPoint.value.x, currentX);
  const y2 = Math.max(startPoint.value.y, currentY);
  const width = x2 - x1;
  const height = y2 - y1;

  bboxCoordinates.value = { x1, y1, width, height };
  bboxForm.value = { x1: Math.round(x1), y1: Math.round(y1), x2: Math.round(x2), y2: Math.round(y2) };
  console.log('bboxCoordinates', bboxCoordinates.value);
};


const stopDrawing = () => {
  if (isDrawing.value && bboxCoordinates.value) {
    // 鼠标松开时，确保 bboxForm 是最终坐标
    bboxForm.value = {
      x1: Math.round(bboxCoordinates.value.x1),
      y1: Math.round(bboxCoordinates.value.y1),
      x2: Math.round(bboxCoordinates.value.x1 + bboxCoordinates.value.width),
      y2: Math.round(bboxCoordinates.value.y1 + bboxCoordinates.value.height)
    };
  }
  isDrawing.value = false;
}

// 获取分类文本
const getCategoryText = (category) => {
  const map = {
    '[0]': '井盖完好',
    '[1]': '井盖破损',
    '[2]': '井盖缺失',
    '[3]': '井盖未盖',
    '[4]': '井圈问题'
  }
  return map[category] || '未分类'
}

// 获取分类标签类型
const getCategoryTagType = (category) => {
  const map = {
    '[0]': 'success',
    '[1]': 'warning',
    '[2]': 'danger',
    '[3]': 'danger',
    '[4]': 'warning'
  }
  return map[category] || 'info'
}

// 提交标注
const submitAnnotation = async () => {
  if (!selectedRow.value) return
  
  isSubmitting.value = true
  
  try {
    // 构建提交数据
    const data = {
      id: selectedRow.value.id,
      category: selectedCategory.value,
      bbox: `${bboxForm.value.x1},${bboxForm.value.y1},${bboxForm.value.x2},${bboxForm.value.y2}`,
      user: '当前用户' // 实际应用中应该是登录用户
    }
    
    // 发送请求
    await axios.put('/well/updateAnnotation', data)
    
    // 显示成功消息
    ElMessage.success('标注信息修改成功')

    // 关键：重新请求最新数据
    const token = sessionStorage.getItem('token')
    const res = await axios.get('/well/wellApi', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    tableData.value = res.data.wellData  // 用最新数据覆盖
    
    // 返回第一步
    goToStep(1)
  } catch (error) {
    console.error('修改失败', error)
    ElMessage.error('修改失败，请重试')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.container {
  display: flex;
  min-height: 100vh;
  background-color: #f5f7fa;
}

/* 左侧导航轴样式 */
.left-sidebar {
  width: 120px;
  background-color: #fff;
  padding: 40px 0;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: center;
}

.steps-axis {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.axis-line {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  background-color: #e5e7eb;
  z-index: 1;
}

.step-item {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 60px;
  cursor: pointer;
  transition: all 0.3s;
}

.step-item:last-child {
  margin-bottom: 0;
}

.step-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #e5e7eb;
  margin-bottom: 10px;
  transition: all 0.3s;
}

.step-label {
  font-size: 14px;
  color: #666;
  transition: all 0.3s;
  white-space: nowrap;
}

.step-item.active .step-dot {
  background-color: #409eff;
  box-shadow: 0 0 0 4px rgba(64, 158, 255, 0.2);
}

.step-item.active .step-label {
  color: #409eff;
  font-weight: 500;
}

/* 右侧内容区域样式 */
.right-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.page-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 30px;
  font-weight: 600;
}

/* 步骤内容样式 */
.content-wrapper {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 30px;
}

.content-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.content-header h2 {
  font-size: 18px;
  color: #333;
  margin-bottom: 5px;
}

.content-header p {
  color: #666;
  font-size: 14px;
}

.content-body {
  display: flex;
  gap: 20px;
}

.image-container {
  flex: 1;
  min-height: 400px;
  background-color: #f9f9f9;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

.placeholder {
  color: #999;
  font-size: 14px;
  text-align: center;
  padding: 20px;
}

.well-image {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
  cursor: crosshair;
  position: relative;
  z-index: 1;
}

.options-container, .bbox-info {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  z-index: 10; /* 确保在图片上方 */
}

.category-radios {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.next-btn {
  margin-top: auto;
  align-self: flex-end;
}

.btn-group {
  display: flex;
  gap: 10px;
  margin-top: auto;
  align-self: flex-end;
}

.bbox-form {
  margin-top: 10px;
}

/* 标注框样式 */
.annotation-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  display: inline-block;
}

.bbox {
  position: absolute;
  border: 2px solid blue;
  background-color: rgba(64, 158, 255, 0.1);
  pointer-events: none;
  z-index: 999; /* 数值只要大于 0 即可，10 是为了预留后续扩展空间 */
}

/* 提交步骤样式 */
.summary-card {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 20px;
  width: 100%;
}

.summary-item {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.summary-item .label {
  font-weight: 500;
  width: 80px;
}

.thumbnail {
  width: 100px;
  height: auto;
  border-radius: 4px;
}

.category-tag {
  margin: 0;
}

/* 表格样式 */
.table-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.selected-row {
  background-color: #f0f7ff;
}

/* 响应式调整 */
@media (max-width: 992px) {
  .content-body {
    flex-direction: column;
  }
  
  .options-container, .bbox-info {
    width: 100%;
  }
}
</style>