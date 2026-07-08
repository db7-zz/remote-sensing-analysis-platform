<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

import { uploadImage } from '../api/files'
import { createTask, type CreateTaskPayload } from '../api/tasks'
import { TASK_TYPE_OPTIONS } from '../constants/tasks'
import ImageUploader from '../components/ImageUploader.vue'

const router = useRouter()
const submitting = ref(false)
const selectedFile = ref<File | null>(null)
const uploadProgress = ref(0)
const confidence = ref(0.25)
const form = reactive<CreateTaskPayload>({
  name: '',
  task_type: 'object_detection',
  model_key: 'yolo11n',
  parameters: {},
})

async function submitTask() {
  if (!form.name.trim()) {
    ElMessage.warning('请输入任务名称')
    return
  }
  if (!selectedFile.value) {
    ElMessage.warning('请先选择一张遥感图片')
    return
  }

  submitting.value = true
  uploadProgress.value = 0
  try {
    const uploadedFile = await uploadImage(selectedFile.value, (percentage) => {
      uploadProgress.value = percentage
    })
    const task = await createTask({
      ...form,
      name: form.name.trim(),
      parameters: { confidence: confidence.value },
      input_file_ids: [uploadedFile.id],
    })
    if (task.status === 'completed') {
      ElMessage.success('真实 YOLO 目标检测已完成')
    } else if (task.status === 'failed') {
      ElMessage.error(task.error_message || '目标检测失败')
    }
    await router.push(`/tasks/${task.id}`)
  } catch (error) {
    const message = axios.isAxiosError(error)
      ? error.response?.data?.message
      : null
    ElMessage.error(message || '创建任务失败，请确认后端和数据库已经启动')
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
      title="阶段 4：真实 YOLO 目标检测"
      description="当前仅目标检测可执行；使用通用 YOLO11n 权重验证工程闭环，不代表遥感专项检测精度。其他分析类型仍为 planned。"
      type="success"
      :closable="false"
      show-icon
    />

    <div class="form-panel">
      <el-form label-position="top" @submit.prevent="submitTask">
        <el-form-item label="输入图片" required>
          <ImageUploader
            v-model="selectedFile"
            :uploading="submitting"
            :progress="uploadProgress"
          />
        </el-form-item>
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
              :disabled="option.value !== 'object_detection'"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="模型">
          <el-input v-model="form.model_key" disabled />
        </el-form-item>
        <el-form-item label="置信度阈值">
          <el-slider
            v-model="confidence"
            :min="0.05"
            :max="0.95"
            :step="0.05"
            show-input
          />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="submitting">
          {{ submitting ? '上传并执行真实推理…' : '上传图片并开始目标检测' }}
        </el-button>
      </el-form>
    </div>
  </section>
</template>
