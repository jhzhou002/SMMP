<template>
  <div class="project-detail" v-if="currentProject">
    <div class="detail-header">
      <el-button @click="$router.go(-1)" style="margin-right: 16px;">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <div class="project-info">
        <h2>{{ currentProject.name }}</h2>
        <el-tag :type="getStatusType(currentProject.status)">
          {{ getStatusText(currentProject.status) }}
        </el-tag>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card title="项目进度" class="progress-card">
          <div class="progress-section">
            <div class="progress-info">
              <span>总体进度</span>
              <span class="progress-percentage">{{ currentProject.progress || 0 }}%</span>
            </div>
            <el-progress :percentage="currentProject.progress || 0" />
          </div>
          
          <div class="agent-status">
            <h4>智能体状态</h4>
            <div class="agent-grid">
              <div class="agent-item" v-for="agent in agents" :key="agent.name">
                <div class="agent-avatar">
                  <el-icon><User /></el-icon>
                </div>
                <div class="agent-info">
                  <div class="agent-name">{{ agent.name }}</div>
                  <div class="agent-status-text" :class="agent.status">{{ agent.statusText }}</div>
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <el-card title="生成的文件" class="files-card">
          <div class="file-list" v-if="projectFiles.length > 0">
            <div class="file-item" v-for="file in projectFiles" :key="file.id">
              <el-icon><Document /></el-icon>
              <span class="file-name">{{ file.fileName }}</span>
              <span class="file-path">{{ file.filePath }}</span>
              <span class="file-author">by {{ file.createdBy }}</span>
            </div>
          </div>
          <el-empty v-else description="暂无生成的文件" />
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card title="实时日志" class="logs-card">
          <div class="logs-container">
            <div class="log-controls">
              <el-button size="small" @click="clearLogs">清空日志</el-button>
              <el-button size="small" @click="autoScroll = !autoScroll" 
                        :type="autoScroll ? 'primary' : 'default'">
                自动滚动
              </el-button>
            </div>
            <div class="logs-list" ref="logsContainer">
              <div class="log-item" v-for="log in agentLogs" :key="log.id">
                <div class="log-header">
                  <span class="log-agent">{{ log.agentName }}</span>
                  <span class="log-time">{{ formatTime(log.timestamp) }}</span>
                </div>
                <div class="log-message">{{ log.message }}</div>
              </div>
              <div v-if="agentLogs.length === 0" class="no-logs">
                暂无日志信息
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
  <div v-else class="loading">
    <el-loading />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import socketService from '@/services/socket'
import { ArrowLeft, User, Document } from '@element-plus/icons-vue'

const route = useRoute()
const projectStore = useProjectStore()

const currentProject = computed(() => projectStore.currentProject)
const agentLogs = computed(() => projectStore.agentLogs)
const autoScroll = ref(true)
const logsContainer = ref()
const projectFiles = ref([])

const agents = ref([
  { name: 'ProductManager', status: 'idle', statusText: '待机中' },
  { name: 'Architect', status: 'idle', statusText: '待机中' },
  { name: 'Engineer', status: 'idle', statusText: '待机中' }
])

const getStatusType = (status: string) => {
  const statusMap: Record<string, any> = {
    'initializing': 'info',
    'requirement_analysis': 'warning',
    'designing': 'warning',
    'coding': 'warning',
    'testing': 'warning',
    'completed': 'success',
    'error': 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'initializing': '初始化中',
    'requirement_analysis': '需求分析',
    'designing': '设计阶段',
    'coding': '编码中',
    'testing': '测试中',
    'completed': '已完成',
    'error': '错误'
  }
  return statusMap[status] || '未知状态'
}

const formatTime = (timestamp: Date) => {
  return new Intl.DateTimeFormat('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(timestamp)
}

const clearLogs = () => {
  projectStore.clearLogs()
}

const scrollToBottom = () => {
  if (autoScroll.value && logsContainer.value) {
    nextTick(() => {
      logsContainer.value.scrollTop = logsContainer.value.scrollHeight
    })
  }
}

watch(agentLogs, () => {
  scrollToBottom()
}, { deep: true })

onMounted(async () => {
  const projectId = route.params.id as string
  try {
    await projectStore.getProject(projectId)
    socketService.joinProject(projectId)
  } catch (error) {
    console.error('Failed to load project:', error)
  }
})

onUnmounted(() => {
  const projectId = route.params.id as string
  socketService.leaveProject(projectId)
})
</script>

<style scoped>
.project-detail {
  padding: 20px;
}

.detail-header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.project-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.project-info h2 {
  margin: 0;
  color: #303133;
}

.progress-card {
  margin-bottom: 20px;
}

.progress-section {
  margin-bottom: 24px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.progress-percentage {
  font-weight: bold;
  color: #409eff;
}

.agent-status h4 {
  margin: 0 0 16px 0;
  color: #303133;
}

.agent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.agent-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  background: #fafafa;
}

.agent-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #409eff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 12px;
}

.agent-name {
  font-weight: bold;
  color: #303133;
}

.agent-status-text {
  font-size: 12px;
  color: #909399;
}

.agent-status-text.active {
  color: #67c23a;
}

.files-card {
  margin-bottom: 20px;
}

.file-list {
  max-height: 300px;
  overflow-y: auto;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f5f7fa;
}

.file-item:last-child {
  border-bottom: none;
}

.file-name {
  font-weight: bold;
  margin-left: 8px;
  color: #303133;
}

.file-path {
  margin-left: auto;
  color: #909399;
  font-size: 12px;
}

.file-author {
  margin-left: 16px;
  color: #909399;
  font-size: 12px;
}

.logs-card {
  height: calc(100vh - 200px);
}

.logs-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.log-controls {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.logs-list {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 12px;
  background: #fafafa;
}

.log-item {
  margin-bottom: 12px;
  padding: 8px;
  background: white;
  border-radius: 4px;
  border-left: 3px solid #409eff;
}

.log-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.log-agent {
  font-weight: bold;
  color: #409eff;
}

.log-time {
  font-size: 12px;
  color: #909399;
}

.log-message {
  color: #303133;
  line-height: 1.4;
}

.no-logs {
  text-align: center;
  color: #909399;
  padding: 20px;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}
</style>