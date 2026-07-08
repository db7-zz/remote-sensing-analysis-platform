<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'

const props = defineProps<{
  modelValue: File | null
  uploading: boolean
  progress: number
}>()

const emit = defineEmits<{
  'update:modelValue': [file: File | null]
}>()

const input = ref<HTMLInputElement | null>(null)
const previewUrl = ref('')

function revokePreview() {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = ''
  }
}

watch(
  () => props.modelValue,
  (file) => {
    revokePreview()
    if (file) previewUrl.value = URL.createObjectURL(file)
  },
  { immediate: true },
)

function chooseFile() {
  if (!props.uploading) input.value?.click()
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  if (!['image/jpeg', 'image/png'].includes(file.type)) {
    ElMessage.error('只支持 JPEG 和 PNG 图片')
    target.value = ''
    return
  }
  if (file.size > 20 * 1024 * 1024) {
    ElMessage.error('图片不能超过 20 MB')
    target.value = ''
    return
  }
  emit('update:modelValue', file)
}

function clearFile() {
  emit('update:modelValue', null)
  if (input.value) input.value.value = ''
}

onBeforeUnmount(revokePreview)
</script>

<template>
  <div class="image-uploader" :class="{ 'has-image': previewUrl }">
    <input
      ref="input"
      class="native-file-input"
      type="file"
      accept="image/jpeg,image/png,.jpg,.jpeg,.png"
      @change="handleFileChange"
    />

    <button v-if="!previewUrl" class="upload-dropzone" type="button" @click="chooseFile">
      <el-icon><Picture /></el-icon>
      <strong>选择遥感图片</strong>
      <span>支持 JPEG、PNG，单张不超过 20 MB</span>
    </button>

    <div v-else class="upload-preview">
      <img :src="previewUrl" alt="待上传图片预览" />
      <div class="preview-meta">
        <div>
          <strong>{{ modelValue?.name }}</strong>
          <span>{{ ((modelValue?.size || 0) / 1024 / 1024).toFixed(2) }} MB</span>
        </div>
        <el-button v-if="!uploading" plain size="small" @click="clearFile">重新选择</el-button>
      </div>
      <el-progress v-if="uploading" :percentage="progress" :stroke-width="8" />
    </div>
  </div>
</template>

