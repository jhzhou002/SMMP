export interface Project {
  id: string
  name: string
  description: string
  projectType: string
  requirements: string[]
  status: string
  progress?: number
  createdAt: string
  updatedAt: string
}

export interface AgentLog {
  id: string
  projectId: string
  agentName: string
  message: string
  timestamp: Date
  logType: 'info' | 'error' | 'warning'
}

export interface ProjectFile {
  id: string
  projectId: string
  filePath: string
  fileName: string
  content: string
  fileType: string
  createdBy: string
  createdAt: string
}

export interface CreateProjectRequest {
  name: string
  description: string
  projectType: string
  requirements: string[]
}