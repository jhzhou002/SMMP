import { DatabaseService } from './DatabaseService'
import { v4 as uuidv4 } from 'uuid'
import { logger } from '../middleware/logger'

export interface Project {
  id: string
  name: string
  description: string
  projectType: string
  requirements: string[]
  status: string
  progress?: number
  createdAt: Date
  updatedAt: Date
}

export interface ProjectFile {
  id: string
  projectId: string
  filePath: string
  fileName: string
  content: string
  fileType: string
  createdBy: string
  createdAt: Date
}

export interface CreateProjectData {
  name: string
  description: string
  projectType: string
  requirements: string[]
  status: string
}

export class ProjectService {
  async create(data: CreateProjectData): Promise<Project> {
    const db = DatabaseService.getDatabase()
    const id = uuidv4()
    const now = new Date()

    const query = `
      INSERT INTO projects (id, name, description, project_type, requirements, status, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING *
    `
    
    const values = [
      id,
      data.name,
      data.description,
      data.projectType,
      JSON.stringify(data.requirements),
      data.status,
      now,
      now
    ]

    try {
      const result = await db.query(query, values)
      const project = this.mapRowToProject(result.rows[0])
      logger.info(`Project created in database: ${id}`)
      return project
    } catch (error) {
      logger.error('Database error creating project:', error)
      throw new Error('Failed to create project')
    }
  }

  async getAll(): Promise<Project[]> {
    const db = DatabaseService.getDatabase()
    const query = 'SELECT * FROM projects ORDER BY created_at DESC'

    try {
      const result = await db.query(query)
      return result.rows.map(row => this.mapRowToProject(row))
    } catch (error) {
      logger.error('Database error getting projects:', error)
      throw new Error('Failed to get projects')
    }
  }

  async getById(id: string): Promise<Project | null> {
    const db = DatabaseService.getDatabase()
    const query = 'SELECT * FROM projects WHERE id = $1'

    try {
      const result = await db.query(query, [id])
      if (result.rows.length === 0) {
        return null
      }
      return this.mapRowToProject(result.rows[0])
    } catch (error) {
      logger.error('Database error getting project:', error)
      throw new Error('Failed to get project')
    }
  }

  async updateStatus(id: string, status: string, progress?: number): Promise<void> {
    const db = DatabaseService.getDatabase()
    const query = `
      UPDATE projects 
      SET status = $1, progress = $2, updated_at = $3
      WHERE id = $4
    `

    try {
      await db.query(query, [status, progress, new Date(), id])
      logger.info(`Project ${id} status updated to ${status}`)
    } catch (error) {
      logger.error('Database error updating project status:', error)
      throw new Error('Failed to update project status')
    }
  }

  async getFiles(projectId: string): Promise<ProjectFile[]> {
    const db = DatabaseService.getDatabase()
    const query = 'SELECT * FROM project_files WHERE project_id = $1 ORDER BY created_at DESC'

    try {
      const result = await db.query(query, [projectId])
      return result.rows.map(row => this.mapRowToProjectFile(row))
    } catch (error) {
      logger.error('Database error getting project files:', error)
      throw new Error('Failed to get project files')
    }
  }

  async addFile(fileData: {
    projectId: string
    filePath: string
    fileName: string
    content: string
    fileType: string
    createdBy: string
  }): Promise<ProjectFile> {
    const db = DatabaseService.getDatabase()
    const id = uuidv4()
    const now = new Date()

    const query = `
      INSERT INTO project_files (id, project_id, file_path, file_name, content, file_type, created_by, created_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING *
    `

    const values = [
      id,
      fileData.projectId,
      fileData.filePath,
      fileData.fileName,
      fileData.content,
      fileData.fileType,
      fileData.createdBy,
      now
    ]

    try {
      const result = await db.query(query, values)
      const file = this.mapRowToProjectFile(result.rows[0])
      logger.info(`File added to project ${fileData.projectId}: ${fileData.fileName}`)
      return file
    } catch (error) {
      logger.error('Database error adding file:', error)
      throw new Error('Failed to add file')
    }
  }

  private mapRowToProject(row: any): Project {
    return {
      id: row.id,
      name: row.name,
      description: row.description,
      projectType: row.project_type,
      requirements: typeof row.requirements === 'string' ? JSON.parse(row.requirements) : row.requirements,
      status: row.status,
      progress: row.progress,
      createdAt: row.created_at,
      updatedAt: row.updated_at
    }
  }

  private mapRowToProjectFile(row: any): ProjectFile {
    return {
      id: row.id,
      projectId: row.project_id,
      filePath: row.file_path,
      fileName: row.file_name,
      content: row.content,
      fileType: row.file_type,
      createdBy: row.created_by,
      createdAt: row.created_at
    }
  }
}