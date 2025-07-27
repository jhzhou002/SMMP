import { io, Socket } from 'socket.io-client'
import { useProjectStore } from '@/stores/project'

class SocketService {
  private socket: Socket | null = null
  private store: any = null

  connect() {
    this.socket = io('http://localhost:3001')
    this.store = useProjectStore()
    
    this.socket.on('connect', () => {
      console.log('Connected to server')
      this.store.isConnected = true
    })

    this.socket.on('disconnect', () => {
      console.log('Disconnected from server')
      this.store.isConnected = false
    })

    this.socket.on('connect_error', (error) => {
      console.error('Connection error:', error)
      this.store.isConnected = false
    })
  }

  joinProject(projectId: string) {
    if (this.socket) {
      this.socket.emit('join_project', projectId)
      
      this.socket.on(`project:${projectId}:update`, (data) => {
        console.log('Project update:', data)
        this.store.updateProjectStatus(projectId, data)
      })

      this.socket.on(`project:${projectId}:error`, (error) => {
        console.error('Project error:', error)
      })
    }
  }

  leaveProject(projectId: string) {
    if (this.socket) {
      this.socket.off(`project:${projectId}:update`)
      this.socket.off(`project:${projectId}:error`)
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }
}

export default new SocketService()