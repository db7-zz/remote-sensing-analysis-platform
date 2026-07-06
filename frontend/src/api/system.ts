import { apiClient } from './client'

export interface ApiResponse<T> {
  success: boolean
  code: string
  message: string
  data: T
  request_id: string
}

export interface HealthData {
  service: string
  status: 'healthy'
  version: string
  timestamp: string
}

export async function getHealth(): Promise<ApiResponse<HealthData>> {
  const response = await apiClient.get<ApiResponse<HealthData>>('/health')
  return response.data
}

