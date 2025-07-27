import { Request, Response } from 'express'
import { ProjectService } from '../services/ProjectService'
import { AgentOrchestrator } from '../agents/AgentOrchestrator'
import { logger } from '../middleware/logger'
import Joi from 'joi'

const projectSchema = Joi.object({
  name: Joi.string().min(1).max(100).required(),
  description: Joi.string().min(10).max(1000).required(),
  projectType: Joi.string().valid('web_app', 'api', 'script').required(),
  requirements: Joi.array().items(Joi.string()).max(10)
})

export class ProjectController {
  private projectService: ProjectService
  private agentOrchestrator: AgentOrchestrator

  constructor() {
    this.projectService = new ProjectService()
    this.agentOrchestrator = new AgentOrchestrator()
  }

  async createProject(req: Request, res: Response): Promise<void> {
    try {
      const { error, value } = projectSchema.validate(req.body)
      if (error) {
        res.status(400).json({
          success: false,
          message: error.details[0].message
        })
        return
      }

      const { name, description, projectType, requirements } = value
      
      const project = await this.projectService.create({
        name,
        description,
        projectType,
        requirements: requirements || [],
        status: 'initializing'
      })

      logger.info(`Project created: ${project.id}`)

      this.agentOrchestrator.startProject(project.id, {
        description,
        projectType,
        requirements: requirements || []
      })

      res.json({
        success: true,
        data: project
      })
    } catch (error) {
      logger.error('Failed to create project:', error)
      res.status(500).json({
        success: false,
        message: '创建项目失败'
      })
    }
  }

  async getProjects(req: Request, res: Response): Promise<void> {
    try {
      const projects = await this.projectService.getAll()
      res.json({
        success: true,
        data: projects
      })
    } catch (error) {
      logger.error('Failed to get projects:', error)
      res.status(500).json({
        success: false,
        message: '获取项目列表失败'
      })
    }
  }

  async getProject(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params
      const project = await this.projectService.getById(id)
      
      if (!project) {
        res.status(404).json({
          success: false,
          message: '项目不存在'
        })
        return
      }

      res.json({
        success: true,
        data: project
      })
    } catch (error) {
      logger.error('Failed to get project:', error)
      res.status(500).json({
        success: false,
        message: '获取项目失败'
      })
    }
  }

  async getProjectStatus(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params
      const project = await this.projectService.getById(id)
      
      if (!project) {
        res.status(404).json({
          success: false,
          message: '项目不存在'
        })
        return
      }

      const agentStatus = await this.agentOrchestrator.getStatus(id)
      
      res.json({
        success: true,
        data: {
          ...project,
          agentStatus
        }
      })
    } catch (error) {
      logger.error('Failed to get project status:', error)
      res.status(500).json({
        success: false,
        message: '获取项目状态失败'
      })
    }
  }

  async getProjectFiles(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params
      const files = await this.projectService.getFiles(id)
      
      res.json({
        success: true,
        data: files
      })
    } catch (error) {
      logger.error('Failed to get project files:', error)
      res.status(500).json({
        success: false,
        message: '获取项目文件失败'
      })
    }
  }
}