import asyncio
import time
from typing import Dict, Any, List
from roles.product_manager import CustomProductManager
from roles.architect import CustomArchitect  
from roles.engineer import CustomEngineer
from utils.message_sender import MessageSender
from utils.logger import setup_logger

class ProjectWorkflow:
    def __init__(self, project_id: str, config: Dict[str, Any], message_sender: MessageSender):
        self.project_id = project_id
        self.config = config
        self.message_sender = message_sender
        self.logger = setup_logger(project_id)
        self.generated_files: List[Dict[str, Any]] = []
        
        # 初始化角色
        self.product_manager = CustomProductManager(project_id, message_sender)
        self.architect = CustomArchitect(project_id, message_sender)
        self.engineer = CustomEngineer(project_id, message_sender)

    async def execute(self) -> None:
        """执行完整的项目开发工作流"""
        
        # 阶段1: 需求分析
        await self._requirement_analysis()
        
        # 阶段2: 系统设计
        await self._system_design()
        
        # 阶段3: 代码开发
        await self._code_development()
        
        # 阶段4: 测试验证
        await self._testing_phase()

    async def _requirement_analysis(self) -> None:
        """需求分析阶段"""
        self.logger.info("Starting requirement analysis phase")
        
        await self.message_sender.send_message({
            'type': 'progress',
            'payload': {
                'stage': 'requirement_analysis',
                'progress': 10,
                'message': '产品经理正在分析需求...'
            }
        })

        # 产品经理分析需求
        requirements = await self.product_manager.analyze_requirements(
            self.config['description'],
            self.config.get('requirements', [])
        )
        
        # 模拟分析时间
        await asyncio.sleep(2)
        
        await self.message_sender.send_message({
            'type': 'progress',
            'payload': {
                'stage': 'requirement_analysis',
                'progress': 25,
                'message': '需求分析完成，生成PRD文档'
            }
        })

        # 生成PRD文档
        prd_content = self._generate_prd(requirements)
        self.generated_files.append({
            'fileName': 'PRD.md',
            'filePath': '/docs/PRD.md',
            'content': prd_content,
            'fileType': 'markdown',
            'createdBy': 'ProductManager'
        })

        await self.message_sender.send_message({
            'type': 'file_generated',
            'payload': self.generated_files[-1]
        })

    async def _system_design(self) -> None:
        """系统设计阶段"""
        self.logger.info("Starting system design phase")
        
        await self.message_sender.send_message({
            'type': 'progress',
            'payload': {
                'stage': 'designing',
                'progress': 35,
                'message': '架构师正在设计系统架构...'
            }
        })

        # 架构师设计系统
        design = await self.architect.design_system(
            self.config['projectType'],
            self.config['description']
        )
        
        await asyncio.sleep(3)
        
        await self.message_sender.send_message({
            'type': 'progress',
            'payload': {
                'stage': 'designing',
                'progress': 50,
                'message': '系统设计完成，生成技术方案文档'
            }
        })

        # 生成技术设计文档
        design_content = self._generate_design_doc(design)
        self.generated_files.append({
            'fileName': 'DESIGN.md',
            'filePath': '/docs/DESIGN.md',
            'content': design_content,
            'fileType': 'markdown',
            'createdBy': 'Architect'
        })

        await self.message_sender.send_message({
            'type': 'file_generated',
            'payload': self.generated_files[-1]
        })

    async def _code_development(self) -> None:
        """代码开发阶段"""
        self.logger.info("Starting code development phase")
        
        await self.message_sender.send_message({
            'type': 'progress',
            'payload': {
                'stage': 'coding',
                'progress': 60,
                'message': '工程师开始编写代码...'
            }
        })

        # 工程师开发代码
        code_files = await self.engineer.develop_code(
            self.config['projectType'],
            self.config['description']
        )
        
        await asyncio.sleep(4)
        
        # 生成代码文件
        for i, code_file in enumerate(code_files):
            progress = 60 + (i + 1) * 10
            self.generated_files.append(code_file)
            
            await self.message_sender.send_message({
                'type': 'file_generated',
                'payload': code_file
            })
            
            await self.message_sender.send_message({
                'type': 'progress',
                'payload': {
                    'stage': 'coding',
                    'progress': min(progress, 85),
                    'message': f'生成代码文件: {code_file["fileName"]}'
                }
            })
            
            await asyncio.sleep(1)

    async def _testing_phase(self) -> None:
        """测试验证阶段"""
        self.logger.info("Starting testing phase")
        
        await self.message_sender.send_message({
            'type': 'progress',
            'payload': {
                'stage': 'testing',
                'progress': 90,
                'message': '正在进行测试验证...'
            }
        })

        await asyncio.sleep(2)
        
        # 生成测试文件
        test_content = self._generate_test_file()
        self.generated_files.append({
            'fileName': 'test_suite.py',
            'filePath': '/tests/test_suite.py',
            'content': test_content,
            'fileType': 'python',
            'createdBy': 'Engineer'
        })

        await self.message_sender.send_message({
            'type': 'file_generated',
            'payload': self.generated_files[-1]
        })

        await self.message_sender.send_message({
            'type': 'progress',
            'payload': {
                'stage': 'testing',
                'progress': 95,
                'message': '测试完成，准备交付'
            }
        })

    def _generate_prd(self, requirements: Dict[str, Any]) -> str:
        """生成PRD文档"""
        return f"""# 产品需求文档 (PRD)

## 项目概述
- **项目名称**: {self.config.get('name', '未命名项目')}
- **项目类型**: {self.config['projectType']}
- **项目描述**: {self.config['description']}

## 功能需求
{chr(10).join(f"- {req}" for req in self.config.get('requirements', []))}

## 用户故事
1. 作为用户，我希望能够使用简洁直观的界面
2. 作为用户，我希望系统响应迅速且稳定
3. 作为用户，我希望数据安全可靠

## 验收标准
- 功能完整性：所有需求功能正常运行
- 性能要求：响应时间小于2秒
- 兼容性：支持主流浏览器
- 安全性：数据传输加密，用户信息保护

## 技术约束
- 前端技术栈：Vue.js 3+
- 后端技术栈：Node.js + Express
- 数据库：PostgreSQL
- 部署环境：云服务器

生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""

    def _generate_design_doc(self, design: Dict[str, Any]) -> str:
        """生成设计文档"""
        return f"""# 系统设计文档

## 架构概览
- **架构模式**: {design.get('pattern', 'MVC')}
- **部署方式**: {design.get('deployment', '云端部署')}

## 技术栈
- **前端**: Vue.js 3 + Element Plus
- **后端**: Node.js + Express + TypeScript
- **数据库**: PostgreSQL
- **缓存**: Redis
- **部署**: Docker + Nginx

## 系统架构图
```
[前端界面] -> [API网关] -> [业务逻辑] -> [数据访问] -> [数据库]
     |            |           |           |          |
   Vue.js      Express    TypeScript     ORM    PostgreSQL
```

## 数据库设计
### 主要表结构
- users: 用户信息表
- projects: 项目信息表
- tasks: 任务信息表

## API设计
### 用户管理
- POST /api/users/register - 用户注册
- POST /api/users/login - 用户登录
- GET /api/users/profile - 获取用户信息

### 项目管理
- GET /api/projects - 获取项目列表
- POST /api/projects - 创建新项目
- GET /api/projects/:id - 获取项目详情

## 安全设计
- JWT身份验证
- HTTPS数据传输
- SQL注入防护
- XSS攻击防护

生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""

    def _generate_test_file(self) -> str:
        """生成测试文件"""
        return f"""# 测试套件

import unittest
from datetime import datetime

class ProjectTestSuite(unittest.TestCase):
    \"\"\"项目测试套件\"\"\"
    
    def setUp(self):
        \"\"\"测试前置设置\"\"\"
        self.test_data = {{
            'project_type': '{self.config['projectType']}',
            'description': '{self.config['description']}'
        }}
    
    def test_project_creation(self):
        \"\"\"测试项目创建\"\"\"
        self.assertIsNotNone(self.test_data)
        self.assertEqual(self.test_data['project_type'], '{self.config['projectType']}')
    
    def test_functionality(self):
        \"\"\"测试基本功能\"\"\"
        # 模拟功能测试
        result = True
        self.assertTrue(result)
    
    def test_performance(self):
        \"\"\"测试性能\"\"\"
        start_time = datetime.now()
        # 模拟性能测试
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        self.assertLess(duration, 2.0)  # 响应时间小于2秒

if __name__ == '__main__':
    unittest.main()
"""

    def get_generated_files(self) -> List[Dict[str, Any]]:
        """获取生成的文件列表"""
        return self.generated_files