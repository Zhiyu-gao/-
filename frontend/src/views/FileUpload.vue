<template>
  <div style="padding: 20px;">
    <el-upload
      ref="uploadRef"
      class="upload-demo"
      name="upload_file"  
      action="http://localhost:8000/well/upload" 
      :auto-upload="false" 
      list-type="picture"
      :on-success="handleSuccess"
    >
      <template #trigger>
        <el-button type="primary">选择图片</el-button>
      </template>
      <el-button type="success" @click="submitUpload" style="margin-left: 10px;">
        上传并检测
      </el-button>
    </el-upload>

    <!-- 显示结果 -->
    <div v-if="imageUrl" style="margin-top: 20px;">
      <h3>检测结果：</h3>
      <img :src="imageUrl" style="max-height: 300px;" />
      <p>状态：{{ labelText }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const uploadRef = ref()
const imageUrl = ref('')
const labelText = ref('')

// 提交上传
const submitUpload = () => {
  uploadRef.value.submit()
}

// 上传成功回调
const handleSuccess = (response) => {
  imageUrl.value = response.path  // 图片路径
  // 转换状态文本
  const labelMap = {
    '[0]': '井盖完好',
    '[1]': '井盖破损',
    '[2]': '井盖缺失',
    '[3]': '井盖未盖',
    '[4]': '井圈问题'
  }
  labelText.value = labelMap[response.label] || '未知状态'
}
</script>