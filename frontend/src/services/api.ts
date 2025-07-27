import axios from 'axios'
import type { Project, CreateProjectRequest } from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const projectApi = {
  create: (data: CreateProjectRequest) => api.post<Project>('/projects', data),
  getAll: () => api.get<Project[]>('/projects'),
  getById: (id: string) => api.get<Project>(`/projects/${id}`),
  getFiles: (id: string) => api.get(`/projects/${id}/files`),
  getStatus: (id: string) => api.get(`/projects/${id}/status`)
}

export default api