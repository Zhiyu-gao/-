<template>
  <div class="warning-container">
    <!-- 左侧图片和信息区域（调整为左侧主区域） -->
    <div class="left-panel" v-if="selectedRow">
      <!-- 图片容器，控制图片大小 -->
      <div class="image-container">
        <img 
          :src="`/static/${selectedRow.img}.jpg`"
          alt="井盖图像" 
          class="cover-img"
          @error="handleImgError"
        />
      </div>
      <div class="hidden-type">
        <p>隐患类型：{{ categoryMap[selectedRow.category] || selectedRow.category }}</p>
        <p>ID：{{ selectedRow.id }}</p>
        <p>时间：{{ selectedRow.time }}</p>
        <p>点位：{{ selectedRow.position }}</p>
      </div>
    </div>
    <!-- 未选择行时的提示 -->
    <div class="left-panel empty-state" v-else>
      <p>请从右侧表格选择一条记录查看详情</p>
    </div>

    <!-- 右侧数据列表区域（调整宽度） -->
    <el-table
      :data="tableData"
      style="width: 60%;"
      @row-click="handleRowClick"
      border
      stripe
      class="table-container"
    >
      <el-table-column prop="id" label="ID" width="120" />
      <el-table-column prop="time" label="时间" width="180" />
      <el-table-column prop="position" label="点位" />
      <el-table-column label="类别" width="150">
        <template #default="scope">
          {{ categoryMap[scope.row.category] || scope.row.category }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { ElTable, ElTableColumn, ElMessage } from 'element-plus'

const tableData = ref([])
const selectedRow = ref(null)
const axios = inject('axios');

// 隐患类型映射表
const categoryMap = {
  '0': '井盖完好',
  '1': '井盖破损',
  '2': '井盖缺失',
  '3': '井盖未盖',
  '4': '井圈问题'
};

// 加载数据
onMounted(async () => {
  try {
    const res = await axios.get('/well/monitor/')
    tableData.value = res.data
  } catch (error) {
    console.error('数据加载失败', error)
    ElMessage.error('数据加载失败，请重试')
  }
})

// 处理行点击
const handleRowClick = (row) => {
  selectedRow.value = row
}

// 图片加载失败处理
const handleImgError = (e) => {
  e.target.src = '/static/default-cover.jpg'
  ElMessage.warning('图片加载失败')
}
</script>

<style scoped>
.warning-container {
  display: flex;
  padding: 20px;
  gap: 20px;
  min-height: calc(100vh - 40px);
  box-sizing: border-box;
}

/* 左侧面板调整为40%宽度，确保在左侧显示 */
.left-panel {
  width: 40%;
  padding: 15px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

/* 图片容器控制图片大小 */
.image-container {
  width: 100%;
  /* 限制图片最大宽度和高度，缩小图片尺寸 */
  max-width: 400px;
  max-height: 300px;
  margin: 0 auto 15px; /* 居中显示 */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 图片样式调整 */
.cover-img {
  width: 100%;
  height: auto;
  max-height: 300px; /* 最大高度限制 */
  border-radius: 6px;
  border: 1px solid #f0f0f0;
  object-fit: contain; /* 保持图片比例，不拉伸 */
}

.hidden-type {
  font-size: 16px;
  color: #333;
  padding: 10px;
  background: #fafafa;
  border-radius: 6px;
  line-height: 1.8;
}

/* 未选择数据时的提示样式 */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 350px; /* 与图片区域高度保持一致 */
  color: #999;
  border: 1px dashed #e0e0e0;
}

/* 表格容器样式 */
.table-container {
  height: fit-content;
  max-height: 600px;
  overflow-y: auto;
}

.el-table tr:hover > td {
  background: #f7faff !important;
}

/* 选中行高亮 */
.el-table__row.current-row > td {
  background-color: #e6f7ff !important;
}
</style>
