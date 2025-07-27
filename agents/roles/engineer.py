import asyncio
import time
from typing import Dict, List, Any
from utils.message_sender import MessageSender
from utils.logger import setup_logger

class CustomEngineer:
    """自定义工程师角色"""
    
    def __init__(self, project_id: str, message_sender: MessageSender):
        self.project_id = project_id
        self.message_sender = message_sender
        self.logger = setup_logger(f"{project_id}_engineer")
        self.role_name = "Engineer"

    async def develop_code(self, project_type: str, description: str) -> List[Dict[str, Any]]:
        """开发代码"""
        await self.send_status_update("开始代码开发...")
        
        code_files = []
        
        if project_type == 'web_app':
            code_files.extend(await self._develop_web_app(description))
        elif project_type == 'api':
            code_files.extend(await self._develop_api(description))
        else:  # script
            code_files.extend(await self._develop_script(description))
        
        await self.send_status_update("代码开发完成")
        
        self.logger.info(f"Code development completed for project {self.project_id}")
        return code_files

    async def _develop_web_app(self, description: str) -> List[Dict[str, Any]]:
        """开发Web应用"""
        await self.send_status_update("生成前端组件...")
        await asyncio.sleep(1)
        
        files = []
        
        # 主应用文件
        files.append({
            'fileName': 'App.vue',
            'filePath': '/src/App.vue',
            'content': self._generate_vue_app(description),
            'fileType': 'vue',
            'createdBy': 'Engineer'
        })
        
        # 主页面组件
        files.append({
            'fileName': 'HomePage.vue',
            'filePath': '/src/views/HomePage.vue',
            'content': self._generate_home_page(description),
            'fileType': 'vue',
            'createdBy': 'Engineer'
        })
        
        await self.send_status_update("生成后端API...")
        await asyncio.sleep(1)
        
        # 后端主文件
        files.append({
            'fileName': 'server.js',
            'filePath': '/backend/server.js',
            'content': self._generate_server_js(description),
            'fileType': 'javascript',
            'createdBy': 'Engineer'
        })
        
        # 数据库模型
        files.append({
            'fileName': 'models.js',
            'filePath': '/backend/models.js',
            'content': self._generate_models(description),
            'fileType': 'javascript',
            'createdBy': 'Engineer'
        })
        
        return files

    async def _develop_api(self, description: str) -> List[Dict[str, Any]]:
        """开发API服务"""
        await self.send_status_update("生成API路由...")
        await asyncio.sleep(1)
        
        files = []
        
        # API主文件
        files.append({
            'fileName': 'app.js',
            'filePath': '/src/app.js',
            'content': self._generate_api_app(description),
            'fileType': 'javascript',
            'createdBy': 'Engineer'
        })
        
        # 路由文件
        files.append({
            'fileName': 'routes.js',
            'filePath': '/src/routes.js',
            'content': self._generate_api_routes(description),
            'fileType': 'javascript',
            'createdBy': 'Engineer'
        })
        
        return files

    async def _develop_script(self, description: str) -> List[Dict[str, Any]]:
        """开发脚本工具"""
        await self.send_status_update("生成脚本文件...")
        await asyncio.sleep(1)
        
        files = []
        
        # 主脚本文件
        files.append({
            'fileName': 'main.py',
            'filePath': '/src/main.py',
            'content': self._generate_python_script(description),
            'fileType': 'python',
            'createdBy': 'Engineer'
        })
        
        # 配置文件
        files.append({
            'fileName': 'config.py',
            'filePath': '/src/config.py',
            'content': self._generate_config_file(),
            'fileType': 'python',
            'createdBy': 'Engineer'
        })
        
        return files

    def _generate_vue_app(self, description: str) -> str:
        """生成Vue应用主文件"""
        return f'''<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>{{{{ title }}</h1>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import {{ defineComponent }} from 'vue'

export default defineComponent({{
  name: 'App',
  data() {{
    return {{
      title: '{description[:20]}...'
    }}
  }}
}})
</script>

<style>
#app {{
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}}
</style>'''

    def _generate_home_page(self, description: str) -> str:
        """生成首页组件"""
        return f'''<template>
  <div class="home">
    <el-card>
      <h2>欢迎使用系统</h2>
      <p>{{{{ description }}</p>
      <el-button type="primary" @click="handleStart">开始使用</el-button>
    </el-card>
  </div>
</template>

<script>
import {{ defineComponent }} from 'vue'
import {{ ElMessage }} from 'element-plus'

export default defineComponent({{
  name: 'HomePage',
  data() {{
    return {{
      description: '{description}'
    }}
  }},
  methods: {{
    handleStart() {{
      ElMessage.success('欢迎使用!')
    }}
  }}
}})
</script>

<style scoped>
.home {{
  padding: 20px;
}}
</style>'''

    def _generate_server_js(self, description: str) -> str:
        """生成服务器代码"""
        return f'''const express = require('express')
const cors = require('cors')
const app = express()
const PORT = process.env.PORT || 3001

// 中间件
app.use(cors())
app.use(express.json())

// 路由
app.get('/api/health', (req, res) => {{
  res.json({{ status: 'ok', message: '服务运行正常' }})
}})

app.get('/api/info', (req, res) => {{
  res.json({{
    name: '项目API',
    description: '{description}',
    version: '1.0.0'
  }})
}})

// 启动服务器
app.listen(PORT, () => {{
  console.log(`服务器运行在端口 ${{PORT}}`)
}})

module.exports = app'''

    def _generate_models(self, description: str) -> str:
        """生成数据模型"""
        return '''const { Sequelize, DataTypes } = require('sequelize')

const sequelize = new Sequelize(process.env.DATABASE_URL || 'postgresql://localhost/database')

const User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  username: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  createdAt: {
    type: DataTypes.DATE,
    defaultValue: Sequelize.NOW
  }
})

module.exports = { sequelize, User }'''

    def _generate_api_app(self, description: str) -> str:
        """生成API应用"""
        return f'''const express = require('express')
const cors = require('cors')
const helmet = require('helmet')
const rateLimit = require('express-rate-limit')

const app = express()
const PORT = process.env.PORT || 3001

// 安全中间件
app.use(helmet())
app.use(cors())

// 限流
const limiter = rateLimit({{
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 100 // 限制每个IP 100次请求
}})
app.use(limiter)

// 解析JSON
app.use(express.json())

// 健康检查
app.get('/health', (req, res) => {{
  res.json({{ status: 'healthy', timestamp: new Date().toISOString() }})
}})

// API文档
app.get('/api/docs', (req, res) => {{
  res.json({{
    title: 'API文档',
    description: '{description}',
    version: '1.0.0',
    endpoints: [
      'GET /health - 健康检查',
      'GET /api/docs - API文档'
    ]
  }})
}})

app.listen(PORT, () => {{
  console.log(`API服务运行在端口 ${{PORT}}`)
}})

module.exports = app'''

    def _generate_api_routes(self, description: str) -> str:
        """生成API路由"""
        return '''const express = require('express')
const router = express.Router()

// 用户路由
router.get('/users', (req, res) => {
  res.json({ message: '获取用户列表', users: [] })
})

router.post('/users', (req, res) => {
  const { username, email } = req.body
  res.json({ message: '用户创建成功', user: { username, email } })
})

router.get('/users/:id', (req, res) => {
  const { id } = req.params
  res.json({ message: '获取用户详情', userId: id })
})

module.exports = router'''

    def _generate_python_script(self, description: str) -> str:
        """生成Python脚本"""
        return f'''#!/usr/bin/env python3
"""
{description}

使用方法:
    python main.py [参数]
"""

import argparse
import logging
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='{description}')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info('脚本开始执行...')
    
    # 加载配置
    config = Config(args.config)
    
    # 主要逻辑
    try:
        process_data()
        logger.info('脚本执行完成')
    except Exception as e:
        logger.error(f'执行失败: {{e}}')
        return 1
    
    return 0

def process_data():
    """处理数据的主要逻辑"""
    logger.info('开始处理数据...')
    # 具体的处理逻辑
    pass

if __name__ == '__main__':
    exit(main())'''

    def _generate_config_file(self) -> str:
        """生成配置文件"""
        return '''"""
配置管理模块
"""

import os
import json
from typing import Dict, Any

class Config:
    """配置类"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or 'config.json'
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            'debug': False,
            'log_level': 'INFO',
            'timeout': 30,
            'max_retries': 3
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return {**default_config, **json.load(f)}
            except Exception as e:
                print(f'加载配置文件失败: {e}')
        
        return default_config
    
    def get(self, key: str, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self.config[key] = value
    
    def save(self):
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f'保存配置文件失败: {e}')'''

    async def send_status_update(self, message: str):
        """发送状态更新"""
        await self.message_sender.send_message({
            'type': 'agent_message',
            'payload': {
                'agent': self.role_name,
                'message': message,
                'timestamp': time.time()
            }
        })
        self.logger.info(f"Engineer Status: {message}")