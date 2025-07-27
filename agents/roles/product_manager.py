import asyncio
import time
from typing import Dict, List, Any
from utils.message_sender import MessageSender
from utils.logger import setup_logger

class CustomProductManager:
    """自定义产品经理角色"""
    
    def __init__(self, project_id: str, message_sender: MessageSender):
        self.project_id = project_id
        self.message_sender = message_sender
        self.logger = setup_logger(f"{project_id}_pm")
        self.role_name = "ProductManager"

    async def analyze_requirements(self, description: str, requirements: List[str]) -> Dict[str, Any]:
        """分析项目需求"""
        await self.send_status_update("开始分析项目需求...")
        
        # 模拟需求分析过程
        await asyncio.sleep(1)
        
        await self.send_status_update("解析功能需求...")
        
        # 基于描述和需求生成分析结果
        analysis = {
            'functional_requirements': self._extract_functional_requirements(description, requirements),
            'non_functional_requirements': self._extract_non_functional_requirements(),
            'user_stories': self._generate_user_stories(description),
            'acceptance_criteria': self._generate_acceptance_criteria()
        }
        
        await asyncio.sleep(1)
        await self.send_status_update("需求分析完成，生成PRD文档")
        
        self.logger.info(f"Requirements analysis completed for project {self.project_id}")
        return analysis

    def _extract_functional_requirements(self, description: str, requirements: List[str]) -> List[str]:
        """提取功能需求"""
        functional_reqs = []
        
        # 基于项目描述提取需求
        if "用户" in description:
            functional_reqs.append("用户管理系统")
        if "登录" in description or "认证" in description:
            functional_reqs.append("用户认证功能")
        if "数据" in description:
            functional_reqs.append("数据管理功能")
        if "搜索" in description:
            functional_reqs.append("搜索功能")
        
        # 添加用户提供的需求
        functional_reqs.extend(requirements)
        
        return functional_reqs

    def _extract_non_functional_requirements(self) -> List[str]:
        """提取非功能需求"""
        return [
            "系统响应时间小于2秒",
            "支持并发用户数100+",
            "数据安全加密传输",
            "7x24小时稳定运行",
            "界面友好易用"
        ]

    def _generate_user_stories(self, description: str) -> List[str]:
        """生成用户故事"""
        stories = [
            "作为用户，我希望能够快速注册和登录系统",
            "作为用户，我希望界面简洁直观，操作便捷",
            "作为用户，我希望数据能够安全保存和访问"
        ]
        
        # 根据项目描述添加特定用户故事
        if "管理" in description:
            stories.append("作为管理员，我希望能够管理用户和权限")
        if "分析" in description:
            stories.append("作为用户，我希望能够查看数据分析报告")
        if "通知" in description:
            stories.append("作为用户，我希望能够接收重要通知")
            
        return stories

    def _generate_acceptance_criteria(self) -> List[str]:
        """生成验收标准"""
        return [
            "所有功能模块正常运行",
            "用户界面响应流畅",
            "数据完整性和一致性",
            "安全性测试通过",
            "性能指标达到要求"
        ]

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
        self.logger.info(f"PM Status: {message}")