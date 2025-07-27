import express from 'express'
import { createServer } from 'http'
import { Server } from 'socket.io'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import dotenv from 'dotenv'
import rateLimit from 'express-rate-limit'

import { logger } from './middleware/logger'
import { errorHandler } from './middleware/errorHandler'
import projectRoutes from './routes/projectRoutes'
import { DatabaseService } from './services/DatabaseService'

dotenv.config()

const app = express()
const server = createServer(app)
const io = new Server(server, {
  cors: {
    origin: process.env.FRONTEND_URL || "http://localhost:3000",
    methods: ["GET", "POST"]
  }
})

const PORT = process.env.PORT || 3001

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: '请求过于频繁，请稍后再试'
})

app.use(helmet())
app.use(cors({
  origin: process.env.FRONTEND_URL || "http://localhost:3000",
  credentials: true
}))
app.use(morgan('combined', { stream: { write: (message) => logger.info(message.trim()) } }))
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true }))
app.use('/api', apiLimiter)

app.use('/api/projects', projectRoutes)

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

io.on('connection', (socket) => {
  logger.info(`Client connected: ${socket.id}`)
  
  socket.on('join_project', (projectId: string) => {
    socket.join(`project:${projectId}`)
    logger.info(`Client ${socket.id} joined project: ${projectId}`)
  })

  socket.on('leave_project', (projectId: string) => {
    socket.leave(`project:${projectId}`)
    logger.info(`Client ${socket.id} left project: ${projectId}`)
  })

  socket.on('disconnect', () => {
    logger.info(`Client disconnected: ${socket.id}`)
  })
})

app.use(errorHandler)

const startServer = async () => {
  try {
    await DatabaseService.initialize()
    logger.info('Database connected successfully')
    
    server.listen(PORT, () => {
      logger.info(`Server running on port ${PORT}`)
    })
  } catch (error) {
    logger.error('Failed to start server:', error)
    process.exit(1)
  }
}

startServer()

export { io }
export default app