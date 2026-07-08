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
      input_file_ids: [uploadedFile.id],
    })
    ElMessage.success('图片已上传，任务记录已创建')
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
      title="阶段 3 支持安全图片上传"
      description="图片会经过格式、MIME、大小和真实解码校验，并通过文件 ID 关联任务。当前仍不会调用模型，任务保持 pending。"
      type="info"
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
            />
          </el-select>
        </el-form-item>
        <el-form-item label="模型标识（可选）">
          <el-input v-model="form.model_key" placeholder="尚未接入模型，可暂时留空" />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="submitting">
          上传图片并创建任务
        </el-button>
      </el-form>
    </div>
  </section>
</template>
