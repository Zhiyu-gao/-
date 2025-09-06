import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

// 配置axios
const api = axios.create({
  baseURL: "http://localhost:8000",  // 后端接口地址
  timeout: 5000
})

// 请求拦截器：添加JWT令牌
api.interceptors.request.use(config => {
  const token = sessionStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：处理401未授权
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response && err.response.status === 401) {
      // 跳转到登录页
      router.push('/login')
    }
    return Promise.reject(err)
  }
)

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.provide('axios', api)  // 全局提供axios
app.mount('#app')