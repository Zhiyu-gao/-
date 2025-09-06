<template>
  <div id="app">
    <!-- 全局导航栏 -->
    <el-menu
      :default-active="$route.path"
      mode="horizontal"
      style="margin-bottom: 20px;"
      @select="handleMenuSelect"
    >
      <el-menu-item index="/well-list">井盖训练数据管理</el-menu-item>
      <el-menu-item index="/upload">井盖隐患预测</el-menu-item>
      <el-menu-item index="/monitor">井盖预警管理</el-menu-item>
      <el-menu-item index="/history">井盖预测历史</el-menu-item>
      <el-menu-item index="/label">井盖数据标注</el-menu-item>
      <el-menu-item @click="logout" style="float: right;">退出登录</el-menu-item>
    </el-menu>
    
    <!-- 路由出口 -->
    <router-view />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const handleMenuSelect = (index) => {
  router.push(index)
}

// 退出登录：清除token并跳转到登录页
const logout = () => {
  sessionStorage.removeItem('token')
  router.push('/login')
}
</script>