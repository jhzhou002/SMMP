# 多智能体AI软件开发平台 - 开发文档

## 项目概述

### 项目名称
AI-DevTeam - 智能软件开发团队

### 项目描述
基于多智能体架构的AI软件开发平台，通过自然语言驱动，模拟完整的软件开发团队协作流程，自动完成从需求分析到代码实现的全流程开发。

### 技术架构
- **前端**: Vue 3 + Vite + Element Plus + Tailwind CSS
- **后端**: Node.js + Express + TypeScript
- **多智能体框架**: MetaGPT + LangChain
- **数据库**: PostgreSQL + Redis
- **部署**: 宝塔面板 + PM2 + Nginx

## 项目结构

```
ai-devteam/
├── frontend/                    # Vue前端应用
│   ├── src/
│   │   ├── components/         # 公共组件
│   │   ├── views/             # 页面组件
│   │   ├── stores/            # Pinia状态管理
│   │   ├── services/          # API服务
│   │   └── utils/             # 工具函数
│   ├── public/
│   └── package.json
├── backend/                     # Node.js后端服务
│   ├── src/
│   │   ├── controllers/       # 控制器
│   │   ├── services/          # 业务逻辑
│   │   ├── models/            # 数据模型
│   │   ├── routes/            # 路由定义
│   │   ├── middleware/        # 中间件
│   │   ├── agents/            # 智能体管理
│   │   └── utils/             # 工具函数
│   ├── config/
│   └── package.json
├── agents/                      # Python智能体服务
│   ├── roles/                 # 角色定义
│   ├── workflows/             # 工作流
│   └── requirements.txt
├── docker/                      # Docker配置
├── docs/                        # 文档
└── README.md
```

## 环境准备

### 开发环境要求
- Node.js >= 18.0.0
- Python >= 3.9
- PostgreSQL >= 13
- Redis >= 6.0
- Git

### 依赖安装

#### 前端依赖
```bash
cd frontend
npm install
```

#### 后端依赖
```bash
cd backend
npm install
```

#### Python智能体依赖
```bash
cd agents
pip install -r requirements.txt
```

## 详细技术实现

### 1. 前端架构 (Vue 3)

#### 1.1 项目初始化
```bash
# 创建Vue项目
npm create vue@latest frontend
cd frontend

# 安装依赖
npm install element-plus @element-plus/icons-vue
npm install @vueuse/core pinia axios
npm install tailwindcss postcss autoprefixer
npm install socket.io-client
```

#### 1.2 主要页面结构

**项目管理页面 (ProjectDashboard.vue)**
- 项目列表展示
- 创建新项目表单
- 项目状态实时更新

**项目详情页面 (ProjectDetail.vue)**
- 智能体协作可视化
- 代码文件展示
- 实时日志输出

**代码编辑器 (CodeEditor.vue)**
- 集成Monaco Editor
- 语法高亮和自动补全
- 文件树导航

#### 1.3 状态管理 (Pinia)
```javascript
// stores/project.js
import { defineStore } from 'pinia'
import { projectApi } from '@/services/api'

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [],
    currentProject: null,
    agentLogs: [],
    isConnected: false
  }),
  
  actions: {
    async createProject(projectData) {
      const response = await projectApi.create(projectData)
      this.projects.push(response.data)
      return response.data
    },
    
    async fetchProjects() {
      const response = await projectApi.getAll()
      this.projects = response.data
    },
    
    updateProjectStatus(projectId, status) {
      const project = this.projects.find(p => p.id === projectId)
      if (project) {
        project.status = status
      }
    }
  }
})
```

### 2. 后端架构 (Node.js + Express)

#### 2.1 项目初始化
```bash
# 创建后端项目
mkdir backend && cd backend
npm init -y

# 安装依赖
npm install express typescript @types/node
npm install cors helmet morgan dotenv
npm install pg @types/pg redis socket.io
npm install axios child_process
npm install -D nodemon ts-node @types/express
```

#### 2.2 核心服务实现

**项目控制器 (controllers/ProjectController.ts)**
```typescript
import { Request, Response } from 'express'
import { ProjectService } from '../services/ProjectService'
import { AgentOrchestrator } from '../agents/AgentOrchestrator'

export class ProjectController {
  private projectService: ProjectService
  private agentOrchestrator: AgentOrchestrator

  constructor() {
    this.projectService = new ProjectService()
    this.agentOrchestrator = new AgentOrchestrator()
  }

  async createProject(req: Request, res: Response) {
    try {
      const { name, description, projectType, requirements } = req.body
      
      // 创建项目记录
      const project = await this.projectService.create({
        name,
        description,
        projectType,
        requirements,
        status: 'initializing'
      })

      // 启动智能体工作流
      this.agentOrchestrator.startProject(project.id, {
        description,
        projectType,
        requirements
      })

      res.json({
        success: true,
        data: project
      })
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      })
    }
  }

  async getProjectStatus(req: Request, res: Response) {
    try {
      const { projectId } = req.params
      const project = await this.projectService.getById(projectId)
      const agentStatus = await this.agentOrchestrator.getStatus(projectId)
      
      res.json({
        success: true,
        data: {
          ...project,
          agentStatus
        }
      })
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      })
    }
  }
}
```

**智能体编排器 (agents/AgentOrchestrator.ts)**
```typescript
import { spawn, ChildProcess } from 'child_process'
import { EventEmitter } from 'events'
import { io } from '../app'

export class AgentOrchestrator extends EventEmitter {
  private activeProjects: Map<string, ChildProcess> = new Map()

  async startProject(projectId: string, config: any) {
    try {
      // 启动Python智能体进程
      const pythonProcess = spawn('python', [
        '../agents/main.py',
        '--project-id', projectId,
        '--config', JSON.stringify(config)
      ])

      this.activeProjects.set(projectId, pythonProcess)

      // 监听智能体输出
      pythonProcess.stdout.on('data', (data) => {
        const message = data.toString()
        this.handleAgentMessage(projectId, message)
      })

      pythonProcess.stderr.on('data', (data) => {
        console.error(`Agent Error: ${data}`)
        io.emit(`project:${projectId}:error`, data.toString())
      })

      pythonProcess.on('close', (code) => {
        console.log(`Agent process exited with code ${code}`)
        this.activeProjects.delete(projectId)
      })

    } catch (error) {
      console.error('Failed to start agent:', error)
      throw error
    }
  }

  private handleAgentMessage(projectId: string, message: string) {
    try {
      const data = JSON.parse(message)
      
      // 广播智能体状态更新
      io.emit(`project:${projectId}:update`, data)
      
      // 根据消息类型处理
      switch (data.type) {
        case 'progress':
          this.emit('progress', projectId, data.payload)
          break
        case 'file_generated':
          this.emit('file_generated', projectId, data.payload)
          break
        case 'agent_message':
          this.emit('agent_message', projectId, data.payload)
          break
      }
    } catch (error) {
      console.error('Failed to parse agent message:', error)
    }
  }

  async getStatus(projectId: string) {
    return {
      isRunning: this.activeProjects.has(projectId),
      agents: await this.getAgentStatuses(projectId)
    }
  }
}
```

### 3. Python智能体服务

#### 3.1 主要文件结构
```python
# agents/main.py
import asyncio
import json
import sys
import argparse
from metagpt.software_company import SoftwareCompany
from roles.custom_roles import CustomProductManager, CustomArchitect, CustomEngineer

class ProjectAgent:
    def __init__(self, project_id: str, config: dict):
        self.project_id = project_id
        self.config = config
        self.company = None
        self.setup_company()

    def setup_company(self):
        """初始化软件公司和角色"""
        self.company = SoftwareCompany()
        
        # 添加自定义角色
        self.company.hire([
            CustomProductManager(),
            CustomArchitect(),
            CustomEngineer()
        ])

    async def start_development(self):
        """开始软件开发流程"""
        try:
            # 发送开始消息
            self.send_message({
                'type': 'progress',
                'payload': {
                    'stage': 'requirement_analysis',
                    'progress': 0,
                    'message': '开始需求分析...'
                }
            })

            # 执行开发流程
            result = await self.company.run_project(
                idea=self.config['description'],
                investment=10.0,
                n_round=5
            )

            # 发送完成消息
            self.send_message({
                'type': 'progress',
                'payload': {
                    'stage': 'completed',
                    'progress': 100,
                    'message': '项目开发完成',
                    'files': result.get('files', {})
                }
            })

        except Exception as e:
            self.send_message({
                'type': 'error',
                'payload': {
                    'message': str(e)
                }
            })

    def send_message(self, data: dict):
        """发送消息到Node.js后端"""
        message = json.dumps(data)
        print(message, flush=True)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-id', required=True)
    parser.add_argument('--config', required=True)
    args = parser.parse_args()

    config = json.loads(args.config)
    agent = ProjectAgent(args.project_id, config)
    
    await agent.start_development()

if __name__ == "__main__":
    asyncio.run(main())
```

#### 3.2 自定义角色定义
```python
# agents/roles/custom_roles.py
from metagpt.roles import ProductManager, Architect, Engineer
from metagpt.actions import WritePRD, WriteDesign, WriteCode

class CustomProductManager(ProductManager):
    """自定义产品经理角色"""
    
    async def _act(self) -> str:
        # 发送状态更新
        self.send_status_update("正在分析需求...")
        
        # 执行需求分析
        result = await super()._act()
        
        self.send_status_update("需求分析完成")
        return result

    def send_status_update(self, message: str):
        import json
        update = {
            'type': 'agent_message',
            'payload': {
                'agent': 'ProductManager',
                'message': message,
                'timestamp': time.time()
            }
        }
        print(json.dumps(update), flush=True)
```

### 4. 数据库设计

#### 4.1 PostgreSQL表结构
```sql
-- 项目表
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    project_type VARCHAR(50) NOT NULL,
    requirements JSONB,
    status VARCHAR(50) DEFAULT 'initializing',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 项目文件表
CREATE TABLE project_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    content TEXT,
    file_type VARCHAR(50),
    created_by VARCHAR(100), -- 智能体名称
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 智能体日志表
CREATE TABLE agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    agent_name VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    log_type VARCHAR(50) DEFAULT 'info',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户表（可选）
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. WebSocket实时通信

#### 5.1 后端Socket.IO配置
```typescript
// app.ts
import express from 'express'
import { createServer } from 'http'
import { Server } from 'socket.io'

const app = express()
const server = createServer(app)
const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"]
  }
})

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id)
  
  socket.on('join_project', (projectId) => {
    socket.join(`project:${projectId}`)
    console.log(`Client joined project: ${projectId}`)
  })

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id)
  })
})

export { io }
```

#### 5.2 前端Socket连接
```javascript
// services/socket.js
import { io } from 'socket.io-client'
import { useProjectStore } from '@/stores/project'

class SocketService {
  constructor() {
    this.socket = null
    this.store = useProjectStore()
  }

  connect() {
    this.socket = io('http://localhost:3001')
    
    this.socket.on('connect', () => {
      console.log('Connected to server')
      this.store.isConnected = true
    })

    this.socket.on('disconnect', () => {
      console.log('Disconnected from server')
      this.store.isConnected = false
    })
  }

  joinProject(projectId) {
    if (this.socket) {
      this.socket.emit('join_project', projectId)
      
      // 监听项目更新
      this.socket.on(`project:${projectId}:update`, (data) => {
        this.store.updateProjectStatus(projectId, data)
      })
    }
  }
}

export default new SocketService()
```

## 宝塔部署配置

### 1. 服务器环境准备

#### 1.1 安装基础环境
```bash
# 安装Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装Python
sudo apt-get install python3 python3-pip

# 安装PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# 安装Redis
sudo apt-get install redis-server
```

#### 1.2 数据库配置
```bash
# PostgreSQL配置
sudo -u postgres createuser --interactive
sudo -u postgres createdb ai_devteam

# Redis配置
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### 2. 宝塔面板配置

#### 2.1 站点创建
1. 登录宝塔面板
2. 创建站点：ai-devteam.com
3. 设置运行目录：/www/wwwroot/ai-devteam
4. 配置SSL证书（可选）

#### 2.2 Nginx配置
```nginx
# /www/server/panel/vhost/nginx/ai-devteam.com.conf
server {
    listen 80;
    server_name ai-devteam.com;
    
    # 前端静态文件
    location / {
        root /www/wwwroot/ai-devteam/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API代理
    location /api {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # WebSocket代理
    location /socket.io/ {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. PM2进程管理

#### 3.1 PM2配置文件
```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'ai-devteam-backend',
      script: './backend/dist/app.js',
      cwd: '/www/wwwroot/ai-devteam',
      instances: 1,
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
        PORT: 3001,
        DB_HOST: 'localhost',
        DB_PORT: 5432,
        DB_NAME: 'ai_devteam',
        DB_USER: 'ai_devteam_user',
        DB_PASS: 'your_password',
        REDIS_URL: 'redis://localhost:6379'
      },
      error_file: './logs/err.log',
      out_file: './logs/out.log',
      log_file: './logs/combined.log',
      time: true
    }
  ]
}
```

#### 3.2 部署脚本
```bash
#!/bin/bash
# deploy.sh

echo "开始部署AI-DevTeam平台..."

# 1. 拉取最新代码
git pull origin main

# 2. 构建前端
cd frontend
npm install
npm run build
cd ..

# 3. 构建后端
cd backend
npm install
npm run build
cd ..

# 4. 安装Python依赖
cd agents
pip install -r requirements.txt
cd ..

# 5. 重启服务
pm2 restart ecosystem.config.js

echo "部署完成！"
```

## 开发流程

### 1. 本地开发启动

```bash
# 1. 启动数据库服务
sudo systemctl start postgresql
sudo systemctl start redis

# 2. 启动后端服务
cd backend
npm run dev

# 3. 启动前端服务
cd frontend
npm run dev

# 4. 测试Python智能体
cd agents
python main.py --project-id test --config '{"description":"测试项目"}'
```

### 2. 功能测试流程

#### 2.1 创建项目测试
```bash
curl -X POST http://localhost:3001/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "待办事项应用",
    "description": "创建一个简单的待办事项管理应用",
    "projectType": "web_app",
    "requirements": ["用户认证", "任务管理", "优先级设置"]
  }'
```

#### 2.2 查询项目状态
```bash
curl http://localhost:3001/api/projects/{project_id}
```

### 3. 性能监控

#### 3.1 日志配置
```javascript
// backend/src/middleware/logger.ts
import winston from 'winston'

export const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
})
```

#### 3.2 性能指标
- API响应时间监控
- 智能体执行时间统计
- 内存和CPU使用率
- 数据库连接池状态

## 安全配置

### 1. API安全
```typescript
// 限流中间件
import rateLimit from 'express-rate-limit'

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 100, // 限制每个IP 100次请求
  message: '请求过于频繁，请稍后再试'
})

app.use('/api', apiLimiter)
```

### 2. 数据验证
```typescript
// 输入验证中间件
import Joi from 'joi'

const projectSchema = Joi.object({
  name: Joi.string().min(1).max(100).required(),
  description: Joi.string().min(10).max(1000).required(),
  projectType: Joi.string().valid('web_app', 'api', 'script').required(),
  requirements: Joi.array().items(Joi.string()).max(10)
})
```

## 监控和维护

### 1. 系统监控
- 使用PM2监控进程状态
- 配置宝塔面板监控告警
- 设置数据库性能监控

### 2. 日志分析
- 错误日志自动分析
- 用户行为统计
- 智能体性能分析

### 3. 备份策略
- 数据库定期备份
- 代码版本控制
- 配置文件备份

## 扩展计划

### 短期优化
1. 添加更多项目模板
2. 优化智能体协作效率
3. 增强代码质量检查

### 中期发展
1. 支持更多编程语言
2. 集成第三方服务
3. 添加团队协作功能

### 长期规划
1. 智能体能力个性化
2. 自动化测试和部署
3. 开放API平台

---

## 总结

本文档提供了完整的多智能体AI软件开发平台实现方案，基于Vue+Node.js技术栈，通过宝塔面板部署到公网。该方案具有以下特点：

- **技术先进**：采用最新的多智能体技术
- **架构清晰**：前后端分离，模块化设计
- **部署简单**：基于宝塔面板，运维成本低
- **扩展性强**：支持多种项目类型和自定义扩展

按照此文档可以在4-6周内完成MVP版本的开发和部署。