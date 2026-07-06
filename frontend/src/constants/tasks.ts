import type { TaskStatus, TaskType } from '../api/tasks'

export const TASK_TYPE_LABELS: Record<TaskType, string> = {
  object_detection: '目标检测',
  land_cover_classification: '土地覆盖分类',
  road_segmentation: '道路提取',
  change_detection: '变化检测',
}

export const TASK_STATUS_LABELS: Record<TaskStatus, string> = {
  pending: '等待中',
  running: '运行中',
  completed: '已完成',
  failed: '失败',
}

export const TASK_STATUS_TAG_TYPES: Record<
  TaskStatus,
  'info' | 'warning' | 'success' | 'danger'
> = {
  pending: 'info',
  running: 'warning',
  completed: 'success',
  failed: 'danger',
}

export const TASK_TYPE_OPTIONS = Object.entries(TASK_TYPE_LABELS).map(([value, label]) => ({
  value: value as TaskType,
  label,
}))

