<template>
  <div class="project-dashboard">
    <div class="dashboard-header">
      <h2>项目管理</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        创建项目
      </el-button>
    </div>

    <div class="project-grid">
      <el-card v-for="project in projects" :key="project.id" class="project-card" @click="goToProject(project.id)">
        <div class="project-header">
          <h3>{{ project.name }}</h3>
          <el-tag :type="getStatusType(project.status)">{{ getStatusText(project.status) }}</el-tag>
        </div>
        <p class="project-description">{{ project.description }}</p>
        <div class="project-type">
          <el-icon><Document /></el-icon>
          <span>{{ getProjectTypeText(project.projectType) }}</span>
        </div>
        <div v-if="project.progress !== undefined" class="project-progress">
          <el-progress :percentage="project.progress" :show-text="false" />
          <span class="progress-text">{{ project.progress }}%</span>
        </div>
      </el-card>
    </div>

    <el-dialog v-model="showCreateDialog" title="创建新项目" width="600px">
      <el-form :model="newProject" label-width="100px" @submit.prevent="createProject">
        <el-form-item label="项目名称" required>
          <el-input v-model="newProject.name" placeholder="输入项目名称" />
        </el-form-item>
        <el-form-item label="项目描述" required>
          <el-input 
            v-model="newProject.description" 
            type="textarea" 
            rows="3"
            placeholder="描述您要开发的项目..." 
          />
        </el-form-item>
        <el-form-item label="项目类型" required>
          <el-select v-model="newProject.projectType" placeholder="选择项目类型">
            <el-option label="Web应用" value="web_app" />
            <el-option label="API服务" value="api" />
            <el-option label="脚本工具" value="script" />
          </el-select>
        </el-form-item>
        <el-form-item label="功能需求">
          <el-tag 
            v-for="requirement in newProject.requirements" 
            :key="requirement"
            closable
            @close="removeRequirement(requirement)"
            style="margin-right: 8px; margin-bottom: 8px;"
          >
            {{ requirement }}
          </el-tag>
          <el-input
            v-if="inputVisible"
            ref="inputRef"
            v-model="inputValue"
            size="small"
            style="width: 100px;"
            @keyup.enter="handleInputConfirm"
            @blur="handleInputConfirm"
          />
          <el-button v-else size="small" @click="showInput">+ 添加需求</el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="createProject" :loading="creating">创建</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { ElMessage } from 'element-plus'
import { Plus, Document } from '@element-plus/icons-vue'

const router = useRouter()
const projectStore = useProjectStore()

const projects = computed(() => projectStore.projects)

const showCreateDialog = ref(false)
const creating = ref(false)
const newProject = ref({
  name: '',
  description: '',
  projectType: '',
  requirements: [] as string[]
})

const inputVisible = ref(false)
const inputValue = ref('')
const inputRef = ref()

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

const getProjectTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    'web_app': 'Web应用',
    'api': 'API服务',
    'script': '脚本工具'
  }
  return typeMap[type] || type
}

const goToProject = (id: string) => {
  router.push(`/project/${id}`)
}

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    inputRef.value?.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value && !newProject.value.requirements.includes(inputValue.value)) {
    newProject.value.requirements.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

const removeRequirement = (requirement: string) => {
  const index = newProject.value.requirements.indexOf(requirement)
  if (index > -1) {
    newProject.value.requirements.splice(index, 1)
  }
}

const createProject = async () => {
  if (!newProject.value.name || !newProject.value.description || !newProject.value.projectType) {
    ElMessage.error('请填写所有必填项')
    return
  }

  creating.value = true
  try {
    await projectStore.createProject(newProject.value)
    ElMessage.success('项目创建成功！')
    showCreateDialog.value = false
    newProject.value = {
      name: '',
      description: '',
      projectType: '',
      requirements: []
    }
  } catch (error) {
    ElMessage.error('项目创建失败')
  } finally {
    creating.value = false
  }
}
</script>

<style scoped>
.project-dashboard {
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-header h2 {
  margin: 0;
  color: #303133;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.project-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.project-header h3 {
  margin: 0;
  color: #303133;
}

.project-description {
  color: #606266;
  margin-bottom: 16px;
  line-height: 1.5;
}

.project-type {
  display: flex;
  align-items: center;
  color: #909399;
  margin-bottom: 16px;
}

.project-type span {
  margin-left: 4px;
}

.project-progress {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-text {
  font-size: 12px;
  color: #909399;
}
</style>