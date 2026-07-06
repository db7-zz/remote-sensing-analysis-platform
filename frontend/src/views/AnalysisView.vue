<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { createTask, type CreateTaskPayload } from '../api/tasks'
import { TASK_TYPE_OPTIONS } from '../constants/tasks'

const router = useRouter()
const submitting = ref(false)
const form = reactive<CreateTaskPayload>({
  name: '',
  task_type: 'object_detection',
  parameters: {},
})

async function submitTask() {
  if (!form.name.trim()) {
    ElMessage.warning('请输入任务名称')
    return
  }

  submitting.value = true
  try {
    const task = await createTask({ ...form, name: form.name.trim() })
    ElMessage.success('任务记录已创建')
    await router.push(`/tasks/${task.id}`)
  } catch {
    ElMessage.error('创建任务失败，请确认后端和数据库已经启动')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section class="page-container workspace-page">
    <div class="page-heading">
      <div>
        <span class="eyebrow">CREATE ANALYSIS TASK</span>
        <h1>创建分析任务</h1>
      </div>
      <RouterLink class="text-link" to="/tasks">查看历史任务 →</RouterLink>
    </div>

    <el-alert
      class="stage-notice"
      title="阶段 2 只创建任务记录"
      description="当前提交不会上传图片或调用模型。新任务会以 pending 状态保存，为后续真实推理流程提供统一入口。"
      type="info"
      :closable="false"
      show-icon
    />

    <div class="form-panel">
      <el-form label-position="top" @submit.prevent="submitTask">
        <el-form-item label="任务名称" required>
          <el-input
            v-model="form.name"
            maxlength="120"
            show-word-limit
            placeholder="例如：港口区域目标检测"
          />
        </el-form-item>
        <el-form-item label="分析类型" required>
          <el-select v-model="form.task_type" class="full-width">
            <el-option
              v-for="option in TASK_TYPE_OPTIONS"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="模型标识（可选）">
          <el-input v-model="form.model_key" placeholder="尚未接入模型，可暂时留空" />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="submitting">
          创建任务记录
        </el-button>
      </el-form>
    </div>
  </section>
</template>

