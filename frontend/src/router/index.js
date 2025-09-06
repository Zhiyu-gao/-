import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import WellList from '../views/WellList.vue'
import FileUpload from '../views/FileUpload.vue'
import WarningList from '../views/WarningList.vue'
import PredictHistory from '../views/PredictHistory.vue'
import DataLabel from '../views/DataLabel.vue'


const routes = [
  { path: '/login', name: 'LoginPage', component: LoginPage },
  { path: '/well-list', name: 'WellList', component: WellList },
  { path: '/upload', name: 'FileUpload', component: FileUpload },
  { path: '/monitor', name: 'WarningList', component: WarningList },
  { path: '/history', name: 'PredictHistory', component: PredictHistory },
  { path: '/label', name: 'DataLabel', component: DataLabel },
  { path: '/', redirect: '/login' }  // 默认跳转登录页
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router