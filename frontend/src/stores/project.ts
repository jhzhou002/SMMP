import { defineStore } from 'pinia'
import { ref } from 'vue'
import { projectApi } from '@/services/api'
import type { Project, AgentLog } from '@/types'

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const agentLogs = ref<AgentLog[]>([])
  const isConnected = ref(false)

  const createProject = async (projectData: any) => {
    try {
      const response = await projectApi.create(projectData)
      projects.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Failed to create project:', error)
      throw error
    }
  }

  const fetchProjects = async () => {
    try {
      const response = await projectApi.getAll()
      projects.value = response.data
    } catch (error) {
      console.error('Failed to fetch projects:', error)
    }
  }

  const getProject = async (id: string) => {
    try {
      const response = await projectApi.getById(id)
      currentProject.value = response.data
      return response.data
    } catch (error) {
      console.error('Failed to fetch project:', error)
      throw error
    }
  }

  const updateProjectStatus = (projectId: string, data: any) => {
    const project = projects.value.find(p => p.id === projectId)
    if (project) {
      project.status = data.payload?.stage || project.status
      project.progress = data.payload?.progress || project.progress
    }
    
    if (currentProject.value?.id === projectId) {
      currentProject.value.status = data.payload?.stage || currentProject.value.status
      currentProject.value.progress = data.payload?.progress || currentProject.value.progress
    }

    if (data.type === 'agent_message') {
      agentLogs.value.push({
        id: Date.now().toString(),
        projectId,
        agentName: data.payload.agent,
        message: data.payload.message,
        timestamp: new Date(data.payload.timestamp * 1000),
        logType: 'info'
      })
    }
  }

  const clearLogs = () => {
    agentLogs.value = []
  }

  return {
    projects,
    currentProject,
    agentLogs,
    isConnected,
    createProject,
    fetchProjects,
    getProject,
    updateProjectStatus,
    clearLogs
  }
})