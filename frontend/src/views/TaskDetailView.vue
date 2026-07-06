<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getTask, type AnalysisTask } from '../api/tasks'
import { TASK_STATUS_LABELS, TASK_STATUS_TAG_TYPES, TASK_TYPE_LABELS } from '../constants/tasks'

const route = useRoute()
const loading = ref(false)
const errorMessage = ref('')
const task = ref<AnalysisTask | null>(null)

function formatDate(value: string | null) {
  if (!value) return '—'
  return new Intl.DateTimeFormat('zh-CN', {
    dateStyle: 'medium',
    timeStyle: 'medium',
  }).format(new Date(value))
}

async function loadTask() {
  loading.value = true
  errorMessage.value = ''
  try {
    task.value = await getTask(String(route.params.id))
  } catch {
    errorMessage.value = '任务不存在、已删除，或后端服务当前不可用。'
  } finally {
    loading.value = false
  }
}

onMounted(loadTask)
</script>

<template>
  <section class="page-container workspace-page">
    <div class="page-heading">
      <div>
        <span class="eyebrow">TASK DETAIL</span>
        <h1>任务详情</h1>
      </div>
      <RouterLink class="text-link" to="/tasks">← 返回历史任务</RouterLink>
    </div>

    <div v-loading="loading" class="detail-panel">
      <el-alert v-if="errorMessage" :title="errorMessage" type="error" :closable="false" show-icon />

      <template v-else-if="task">
        <div class="detail-header">
          <div>
            <small>{{ task.id }}</small>
            <h2>{{ task.name }}</h2>
          </div>
          <el-tag :type="TASK_STATUS_TAG_TYPES[task.status]" size="large">
            {{ TASK_STATUS_LABELS[task.status] }}
          </el-tag>
        </div>

        <el-descriptions :column="2" border>
          <el-descriptions-item label="任务类型">{{ TASK_TYPE_LABELS[task.task_type] }}</el-descriptions-item>
          <el-descriptions-item label="模型标识">{{ task.model_key || '尚未指定' }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(task.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ formatDate(task.updated_at) }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ formatDate(task.started_at) }}</el-descriptions-item>
          <el-descriptions-item label="完成时间">{{ formatDate(task.completed_at) }}</el-descriptions-item>
        </el-descriptions>

        <div class="parameters-block">
          <h3>任务参数</h3>
          <pre>{{ JSON.stringify(task.parameters, null, 2) }}</pre>
        </div>

        <el-alert
          v-if="task.status === 'pending'"
          title="等待后续推理模块处理"
          description="阶段 2 只持久化任务记录。模型接入后，推理服务会把任务从 pending 更新为 running，再进入 completed 或 failed。"
          type="info"
          :closable="false"
          show-icon
        />
      </template>
    </div>
  </section>
</template>

