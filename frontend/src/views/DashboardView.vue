<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Aim, Connection, Grid, MapLocation } from '@element-plus/icons-vue'

import { getHealth, type HealthData } from '../api/system'

type LoadState = 'loading' | 'success' | 'error'

const loadState = ref<LoadState>('loading')
const health = ref<HealthData | null>(null)
const errorMessage = ref('')

const statusLabel = computed(() => {
  if (loadState.value === 'loading') return '正在检查服务'
  if (loadState.value === 'success') return '后端服务正常'
  return '后端暂不可用'
})

async function checkHealth() {
  loadState.value = 'loading'
  errorMessage.value = ''
  try {
    const response = await getHealth()
    health.value = response.data
    loadState.value = 'success'
  } catch {
    health.value = null
    loadState.value = 'error'
    errorMessage.value = '请确认 Flask API 已在 127.0.0.1:5000 启动。'
  }
}

onMounted(checkHealth)

const modules = [
  { title: '目标检测', description: '检测车辆、船只等目标并返回类别、检测框与置信度。', icon: Aim, status: 'planned' },
  { title: '土地覆盖分类', description: '使用视觉特征识别图块中的主导土地覆盖类别。', icon: Grid, status: 'planned' },
  { title: '道路提取', description: '生成道路区域掩膜，并与原始遥感影像进行叠加。', icon: MapLocation, status: 'planned' },
  { title: '变化检测', description: '比较双时相影像，使用可解释 baseline 高亮变化区域。', icon: Connection, status: 'planned' },
]
</script>

<template>
  <section class="hero page-container">
    <div class="eyebrow">PERSONAL ENGINEERING REPRODUCTION</div>
    <h1>让遥感模型成为<br /><span>可理解、可验证的分析流程</span></h1>
    <p>
      基于 Vue 3、Flask 与 PyTorch 构建，从图片上传到模型推理和结果可视化，形成完整的个人演示平台。
    </p>
    <div class="status-card" :class="`status-${loadState}`">
      <span class="status-dot"></span>
      <div>
        <strong>{{ statusLabel }}</strong>
        <small v-if="health">API {{ health.version }} · {{ health.service }}</small>
        <small v-else-if="errorMessage">{{ errorMessage }}</small>
        <small v-else>正在请求健康检查接口…</small>
      </div>
      <el-button v-if="loadState === 'error'" plain size="small" @click="checkHealth">重新检查</el-button>
    </div>
  </section>

  <section class="modules page-container">
    <div class="section-heading">
      <div>
        <span>ANALYSIS MODULES</span>
        <h2>四类遥感分析能力</h2>
      </div>
      <p>所有模块都按真实实现状态标记，规划中的能力不会被描述为已经完成。</p>
    </div>
    <div class="module-grid">
      <article v-for="item in modules" :key="item.title" class="module-card">
        <div class="module-icon"><el-icon><component :is="item.icon" /></el-icon></div>
        <span class="module-status">{{ item.status }}</span>
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
      </article>
    </div>
  </section>
</template>

