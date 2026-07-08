import { apiClient } from './client'
import type { ApiResponse } from './system'

export interface UploadedFileMetadata {
  id: string
  original_name: string
  content_type: string
  extension: string
  size_bytes: number
  width: number
  height: number
  sha256: string
  purpose: string
  content_url: string
  created_at: string
}

export async function uploadImage(
  file: File,
  onProgress?: (percentage: number) => void,
): Promise<UploadedFileMetadata> {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('purpose', 'analysis_input')

  const response = await apiClient.post<ApiResponse<UploadedFileMetadata>>('/files', formData, {
    onUploadProgress: (event) => {
      if (event.total && onProgress) {
        onProgress(Math.round((event.loaded * 100) / event.total))
      }
    },
  })
  return response.data.data
}

