import { spawn, ChildProcess } from 'child_process'
import { EventEmitter } from 'events'
import path from 'path'
import { logger } from '../middleware/logger'
import { ProjectService } from '../services/ProjectService'

const io = require('../app').io

export interface ProjectConfig {
  description: string
  projectType: string
  requirements: string[]
}

export interface AgentStatus {
  isRunning: boolean
  agents: {
    productManager: string
    architect: string
    engineer: string
  }
}

export class AgentOrchestrator extends EventEmitter {
  private activeProjects: Map<string, ChildProcess> = new Map()
  private projectService: ProjectService

  constructor() {
    super()
    this.projectService = new ProjectService()
  }

  async startProject(projectId: string, config: ProjectConfig): Promise<void> {
    try {
      if (this.activeProjects.has(projectId)) {
        logger.warn(`Project ${projectId} is already running`)
        return
      }

      logger.info(`Starting agent process for project: ${projectId}`)
      
      const agentsPath = path.resolve(__dirname, '../../../agents')
      const pythonProcess = spawn('python3', [
        path.join(agentsPath, 'main.py'),
        '--project-id', projectId,
        '--config', JSON.stringify(config)
      ], {
        cwd: agentsPath,
        stdio: ['pipe', 'pipe', 'pipe']
      })

      this.activeProjects.set(projectId, pythonProcess)

      pythonProcess.stdout?.on('data', (data) => {
        const message = data.toString().trim()
        if (message) {
          this.handleAgentMessage(projectId, message)
        }
      })

      pythonProcess.stderr?.on('data', (data) => {
        const errorMessage = data.toString()
        logger.error(`Agent Error for project ${projectId}: ${errorMessage}`)
        
        if (io) {
          io.emit(`project:${projectId}:error`, {
            type: 'error',
            message: errorMessage,
            timestamp: Date.now()
          })
        }
      })

      pythonProcess.on('close', (code) => {
        logger.info(`Agent process for project ${projectId} exited with code ${code}`)
        this.activeProjects.delete(projectId)
        
        if (code === 0) {
          this.projectService.updateStatus(projectId, 'completed', 100)
        } else {
          this.projectService.updateStatus(projectId, 'error', undefined)
        }
      })

      pythonProcess.on('error', (error) => {
        logger.error(`Failed to start agent process for project ${projectId}:`, error)
        this.activeProjects.delete(projectId)
        this.projectService.updateStatus(projectId, 'error', undefined)
        
        if (io) {
          io.emit(`project:${projectId}:error`, {
            type: 'error',
            message: `Failed to start agent process: ${error.message}`,
            timestamp: Date.now()
          })
        }
      })

    } catch (error) {
      logger.error('Failed to start agent process:', error)
      throw error
    }
  }

  private handleAgentMessage(projectId: string, message: string): void {
    try {
      const lines = message.split('\n').filter(line => line.trim())
      
      for (const line of lines) {
        try {
          const data = JSON.parse(line)
          
          logger.info(`Agent message for project ${projectId}:`, data)
          
          if (io) {
            io.emit(`project:${projectId}:update`, data)
          }
          
          switch (data.type) {
            case 'progress':
              this.handleProgressUpdate(projectId, data.payload)
              break
            case 'file_generated':
              this.handleFileGenerated(projectId, data.payload)
              break
            case 'agent_message':
              this.handleAgentLog(projectId, data.payload)
              break
            case 'error':
              this.handleAgentError(projectId, data.payload)
              break
          }
        } catch (parseError) {
          logger.warn(`Failed to parse agent message: ${line}`, parseError)
        }
      }
    } catch (error) {
      logger.error('Failed to handle agent message:', error)
    }
  }

  private async handleProgressUpdate(projectId: string, payload: any): Promise<void> {
    try {
      if (payload.stage && payload.progress !== undefined) {
        await this.projectService.updateStatus(projectId, payload.stage, payload.progress)
      }
      this.emit('progress', projectId, payload)
    } catch (error) {
      logger.error('Failed to handle progress update:', error)
    }
  }

  private async handleFileGenerated(projectId: string, payload: any): Promise<void> {
    try {
      if (payload.fileName && payload.content) {
        await this.projectService.addFile({
          projectId,
          filePath: payload.filePath || payload.fileName,
          fileName: payload.fileName,
          content: payload.content,
          fileType: payload.fileType || 'unknown',
          createdBy: payload.createdBy || 'Agent'
        })
      }
      this.emit('file_generated', projectId, payload)
    } catch (error) {
      logger.error('Failed to handle file generation:', error)
    }
  }

  private handleAgentLog(projectId: string, payload: any): void {
    this.emit('agent_message', projectId, payload)
  }

  private async handleAgentError(projectId: string, payload: any): Promise<void> {
    try {
      await this.projectService.updateStatus(projectId, 'error', undefined)
      this.emit('agent_error', projectId, payload)
    } catch (error) {
      logger.error('Failed to handle agent error:', error)
    }
  }

  async getStatus(projectId: string): Promise<AgentStatus> {
    const isRunning = this.activeProjects.has(projectId)
    
    return {
      isRunning,
      agents: {
        productManager: isRunning ? 'running' : 'idle',
        architect: isRunning ? 'running' : 'idle',
        engineer: isRunning ? 'running' : 'idle'
      }
    }
  }

  async stopProject(projectId: string): Promise<void> {
    const process = this.activeProjects.get(projectId)
    if (process) {
      process.kill('SIGTERM')
      this.activeProjects.delete(projectId)
      logger.info(`Stopped agent process for project: ${projectId}`)
    }
  }

  async stopAllProjects(): Promise<void> {
    for (const [projectId, process] of this.activeProjects) {
      process.kill('SIGTERM')
      logger.info(`Stopped agent process for project: ${projectId}`)
    }
    this.activeProjects.clear()
  }
}