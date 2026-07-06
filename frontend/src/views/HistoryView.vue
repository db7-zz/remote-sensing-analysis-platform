<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

import { deleteTask, getTasks, type AnalysisTask, type TaskListParams } from '../api/tasks'
import {
  TASK_STATUS_LABELS,
  TASK_STATUS_TAG_TYPES,
  TASK_TYPE_LABELS,
  TASK_TYPE_OPTIONS,
} from '../constants/tasks'

const router = useRouter()
const loading = ref(false)
const errorMessage = ref('')
const tasks = ref<AnalysisTask[]>([])
const total = ref(0)
const filters = reactive<TaskListParams>({ page: 1, page_size: 10, status: '', task_type: '' })

function formatDate(value: string) {
  return new Intl.DateTimeFormat('zh-CN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

async function loadTasks() {
  loading.value = true
  errorMessage.value = ''
  try {
    const result = await getTasks(filters)
    tasks.value = result.items
    total.value = result.total
  } catch {
    errorMessage.value = '任务列表加载失败，请确认 Flask API 和数据库迁移状态。'
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  filters.page = 1
  loadTasks()
}

async function confirmDelete(task: AnalysisTask) {
  try {
    await ElMessageBox.confirm(
      `确定从历史记录中删除“${task.name}”吗？后端将执行软删除。`,
      '删除任务',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' },
    )
    await deleteTask(task.id)
    ElMessage.success('任务已删除')
    await loadTasks()
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      ElMessage.error('删除任务失败')
    }
  }
}

onMounted(loadTasks)
</script>

<template>
  <section class="page-container workspace-page">
    <div class="page-heading">
      <div>
        <span class="eyebrow">TASK HISTORY</span>
        <h1>历史任务</h1>
      </div>
      <RouterLink class="primary-link" to="/analysis">创建任务</RouterLink>
    </div>

    <div class="filter-panel">
      <el-select v-model="filters.task_type" placeholder="全部任务类型" clearable @change="applyFilters">
        <el-option
          v-for="option in TASK_TYPE_OPTIONS"
          :key="option.value"
          :label="option.label"
          :value="option.value"
        />
      </el-select>
      <el-select v-model="filters.status" placeholder="全部状态" clearable @change="applyFilters">
        <el-option
          v-for="(label, value) in TASK_STATUS_LABELS"
          :key="value"
          :label="label"
          :value="value"
        />
      </el-select>
      <el-button @click="loadTasks">刷新</el-button>
    </div>

    <el-alert v-if="errorMessage" :title="errorMessage" type="error" :closable="false" show-icon />

    <div class="table-panel">
      <el-table v-loading="loading" :data="tasks" empty-text="暂无任务记录">
        <el-table-column prop="name" label="任务名称" min-width="190" />
        <el-table-column label="任务类型" min-width="150">
          <template #default="scope">{{ TASK_TYPE_LABELS[scope.row.task_type as AnalysisTask['task_type']] }}</template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="TASK_STATUS_TAG_TYPES[scope.row.status as AnalysisTask['status']]">
              {{ TASK_STATUS_LABELS[scope.row.status as AnalysisTask['status']] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" min-width="170">
          <template #default="scope">{{ formatDate(scope.row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="right">
          <template #default="scope">
            <el-button link type="primary" @click="router.push(`/tasks/${scope.row.id}`)">详情</el-button>
            <el-button link type="danger" @click="confirmDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-if="total > Number(filters.page_size)"
        v-model:current-page="filters.page"
        class="pagination"
        background
        layout="prev, pager, next, total"
        :page-size="filters.page_size"
        :total="total"
        @current-change="loadTasks"
      />
    </div>
  </section>
</template>

