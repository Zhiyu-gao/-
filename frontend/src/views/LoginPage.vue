<template>
  <div style="padding: 50px;">
    <el-row>
      <el-col :span="8" :offset="8">
        <h1>登录</h1>
        <el-input v-model="username" placeholder="账号" style="margin: 20px 0;"></el-input>
        <el-input v-model="passwd" type="password" placeholder="密码" style="margin: 20px 0;"></el-input>
        <el-button type="primary" @click="handleLogin" style="width: 100%;">登录</el-button>
        <p style="color: red; margin-top: 10px;">{{ errorMsg }}</p>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'

const axios = inject('axios')
const router = useRouter()
const username = ref('admin')
const passwd = ref('123456')
const errorMsg = ref('')

const handleLogin = async () => {
  try {
    const res = await axios.post('/User/jwtLogin', {
      username: username.value,
      password: passwd.value  // 注意：这里参数名与后端序列化器一致
    })
    // 保存token
    sessionStorage.setItem('token', res.data.token)
    console.log('登录成功',res.data)
    router.push('/monitor')  // 登录成功跳转井盖列表
  } catch (err) {
    errorMsg.value = '账号或密码错误'
  }
}
</script>