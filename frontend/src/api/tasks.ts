import { apiClient } from './client'
import type { UploadedFileMetadata } from './files'
import type { ApiResponse } from './system'

export type TaskType =
  | 'object_detection'
  | 'land_cover_classification'
  | 'road_segmentation'
  | 'change_detection'

export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed'

export interface Detection {
  class_id: number
  class_name: string
  confidence: number
  bbox: { x1: number; y1: number; x2: number; y2: number }
}

export interface TaskResult {
  id: string
  result_type: string
  implementation: 'real_model' | 'baseline' | 'mock'
  model_key: string
  model_version: string | null
  device: string
  data: {
    detection_count: number
    confidence_threshold: number
    detections: Detection[]
  }
  output_file: UploadedFileMetadata | null
  created_at: string
}

export interface AnalysisTask {
  id: string
  name: string
  task_type: TaskType
  status: TaskStatus
  model_key: string | null
  parameters: Record<string, unknown>
  error_code: string | null
  error_message: string | null
  created_at: string
  updated_at: string
  started_at: string | null
  completed_at: string | null
  duration_ms: number | null
  input_files: Array<{
    role: string
    position: number
    file: UploadedFileMetadata
  }>
  results: TaskResult[]
}

export interface TaskListData {
  items: AnalysisTask[]
  page: number
  page_size: number
  total: number
  pages: number
}

export interface CreateTaskPayload {
  name: string
  task_type: TaskType
  model_key?: string
  parameters?: Record<string, unknown>
  input_file_ids?: string[]
}

export interface TaskListParams {
  page?: number
  page_size?: number
  status?: TaskStatus | ''
  task_type?: TaskType | ''
}

export async function createTask(payload: CreateTaskPayload): Promise<AnalysisTask> {
  const response = await apiClient.post<ApiResponse<AnalysisTask>>('/tasks', payload)
  return response.data.data
}

export async function getTasks(params: TaskListParams): Promise<TaskListData> {
  const response = await apiClient.get<ApiResponse<TaskListData>>('/tasks', { params })
  return response.data.data
}

export async function getTask(taskId: string): Promise<AnalysisTask> {
  const response = await apiClient.get<ApiResponse<AnalysisTask>>(`/tasks/${taskId}`)
  return response.data.data
}

export async function deleteTask(taskId: string): Promise<void> {
  await apiClient.delete(`/tasks/${taskId}`)
}
