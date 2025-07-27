import asyncio
import time
from typing import Dict, Any
from utils.message_sender import MessageSender
from utils.logger import setup_logger

class CustomArchitect:
    """自定义架构师角色"""
    
    def __init__(self, project_id: str, message_sender: MessageSender):
        self.project_id = project_id
        self.message_sender = message_sender
        self.logger = setup_logger(f"{project_id}_architect")
        self.role_name = "Architect"

    async def design_system(self, project_type: str, description: str) -> Dict[str, Any]:
        """设计系统架构"""
        await self.send_status_update("开始系统架构设计...")
        
        # 模拟架构设计过程
        await asyncio.sleep(1)
        
        await self.send_status_update("分析技术栈选型...")
        
        # 根据项目类型选择合适的架构
        architecture = {
            'pattern': self._select_architecture_pattern(project_type),
            'tech_stack': self._select_tech_stack(project_type),
            'database_design': self._design_database(description),
            'api_design': self._design_api(description),
            'deployment': self._design_deployment(project_type)
        }
        
        await asyncio.sleep(1)
        await self.send_status_update("系统架构设计完成")
        
        self.logger.info(f"System architecture designed for project {self.project_id}")
        return architecture

    def _select_architecture_pattern(self, project_type: str) -> str:
        """选择架构模式"""
        patterns = {
            'web_app': 'MVC (Model-View-Controller)',
            'api': 'RESTful API + 微服务架构',
            'script': '模块化单体架构'
        }
        return patterns.get(project_type, 'MVC')

    def _select_tech_stack(self, project_type: str) -> Dict[str, str]:
        """选择技术栈"""
        if project_type == 'web_app':
            return {
                'frontend': 'Vue.js 3 + Element Plus + TypeScript',
                'backend': 'Node.js + Express + TypeScript',
                'database': 'PostgreSQL',
                'cache': 'Redis',
                'deployment': 'Docker + Nginx'
            }
        elif project_type == 'api':
            return {
                'backend': 'Node.js + Express + TypeScript',
                'database': 'PostgreSQL',
                'cache': 'Redis',
                'documentation': 'Swagger/OpenAPI',
                'deployment': 'Docker + API Gateway'
            }
        else:  # script
            return {
                'language': 'Python/Node.js',
                'framework': '命令行框架',
                'packaging': 'npm/pip',
                'deployment': '可执行文件'
            }

    def _design_database(self, description: str) -> Dict[str, Any]:
        """设计数据库结构"""
        tables = ['users']  # 基础用户表
        
        # 根据描述添加相关表
        if "项目" in description or "任务" in description:
            tables.extend(['projects', 'tasks'])
        if "文件" in description:
            tables.append('files')
        if "日志" in description or "记录" in description:
            tables.append('logs')
        if "评论" in description or "反馈" in description:
            tables.append('comments')
        
        return {
            'type': 'PostgreSQL',
            'tables': tables,
            'indexes': ['user_id_idx', 'created_at_idx'],
            'constraints': ['foreign_key_constraints', 'unique_constraints']
        }

    def _design_api(self, description: str) -> Dict[str, Any]:
        """设计API接口"""
        endpoints = [
            'GET /api/health',
            'POST /api/auth/login',
            'POST /api/auth/register',
            'GET /api/users/profile'
        ]
        
        # 根据描述添加相关API
        if "项目" in description:
            endpoints.extend([
                'GET /api/projects',
                'POST /api/projects',
                'GET /api/projects/:id',
                'PUT /api/projects/:id',
                'DELETE /api/projects/:id'
            ])
        if "文件" in description:
            endpoints.extend([
                'GET /api/files',
                'POST /api/files/upload',
                'GET /api/files/:id/download'
            ])
        
        return {
            'style': 'RESTful',
            'endpoints': endpoints,
            'authentication': 'JWT Token',
            'documentation': 'Swagger/OpenAPI 3.0'
        }

    def _design_deployment(self, project_type: str) -> Dict[str, Any]:
        """设计部署方案"""
        if project_type == 'web_app':
            return {
                'containerization': 'Docker',
                'orchestration': 'Docker Compose',
                'web_server': 'Nginx',
                'process_manager': 'PM2',
                'monitoring': 'Winston + 系统监控'
            }
        elif project_type == 'api':
            return {
                'containerization': 'Docker',
                'load_balancer': 'Nginx',
                'api_gateway': 'Express Gateway',
                'monitoring': 'Prometheus + Grafana'
            }
        else:  # script
            return {
                'packaging': '可执行文件',
                'distribution': 'npm/pip registry',
                'execution': '命令行直接运行'
            }

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
        self.logger.info(f"Architect Status: {message}")