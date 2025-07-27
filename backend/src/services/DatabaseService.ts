import { Pool, Client } from 'pg'
import { logger } from '../middleware/logger'

export class DatabaseService {
  private static pool: Pool
  private static isInitialized = false

  static async initialize(): Promise<void> {
    if (this.isInitialized) {
      return
    }

    const config = {
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      database: process.env.DB_NAME || 'ai_devteam',
      user: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASS || '',
      max: 10,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    }

    this.pool = new Pool(config)

    try {
      await this.pool.connect()
      await this.createTables()
      this.isInitialized = true
      logger.info('Database service initialized successfully')
    } catch (error) {
      logger.error('Failed to initialize database:', error)
      throw error
    }
  }

  static getDatabase(): Pool {
    if (!this.isInitialized) {
      throw new Error('Database not initialized. Call DatabaseService.initialize() first.')
    }
    return this.pool
  }

  private static async createTables(): Promise<void> {
    const client = await this.pool.connect()
    
    try {
      await client.query('BEGIN')

      const createProjectsTable = `
        CREATE TABLE IF NOT EXISTS projects (
          id UUID PRIMARY KEY,
          name VARCHAR(255) NOT NULL,
          description TEXT,
          project_type VARCHAR(50) NOT NULL,
          requirements JSONB,
          status VARCHAR(50) DEFAULT 'initializing',
          progress INTEGER DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      `

      const createProjectFilesTable = `
        CREATE TABLE IF NOT EXISTS project_files (
          id UUID PRIMARY KEY,
          project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
          file_path VARCHAR(500) NOT NULL,
          file_name VARCHAR(255) NOT NULL,
          content TEXT,
          file_type VARCHAR(50),
          created_by VARCHAR(100),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      `

      const createAgentLogsTable = `
        CREATE TABLE IF NOT EXISTS agent_logs (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
          agent_name VARCHAR(100) NOT NULL,
          message TEXT NOT NULL,
          log_type VARCHAR(50) DEFAULT 'info',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      `

      const createUsersTable = `
        CREATE TABLE IF NOT EXISTS users (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          username VARCHAR(100) UNIQUE NOT NULL,
          email VARCHAR(255) UNIQUE NOT NULL,
          password_hash VARCHAR(255) NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      `

      await client.query(createProjectsTable)
      await client.query(createProjectFilesTable)
      await client.query(createAgentLogsTable)
      await client.query(createUsersTable)

      await client.query('COMMIT')
      logger.info('Database tables created/verified successfully')
    } catch (error) {
      await client.query('ROLLBACK')
      logger.error('Failed to create database tables:', error)
      throw error
    } finally {
      client.release()
    }
  }

  static async close(): Promise<void> {
    if (this.pool) {
      await this.pool.end()
      this.isInitialized = false
      logger.info('Database connection pool closed')
    }
  }
}