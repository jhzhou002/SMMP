import asyncio
import json
import sys
import argparse
import time
import os
from typing import Dict, Any

from workflows.project_workflow import ProjectWorkflow
from utils.logger import setup_logger
from utils.message_sender import MessageSender

class ProjectAgent:
    def __init__(self, project_id: str, config: Dict[str, Any]):
        self.project_id = project_id
        self.config = config
        self.logger = setup_logger(project_id)
        self.message_sender = MessageSender()
        self.workflow = ProjectWorkflow(project_id, config, self.message_sender)

    async def start_development(self) -> None:
        """开始软件开发流程"""
        try:
            self.logger.info(f"Starting development for project {self.project_id}")
            
            # 发送开始消息
            await self.message_sender.send_message({
                'type': 'progress',
                'payload': {
                    'stage': 'initializing',
                    'progress': 0,
                    'message': '初始化开发环境...'
                }
            })

            # 执行完整的开发工作流
            await self.workflow.execute()

            # 发送完成消息
            await self.message_sender.send_message({
                'type': 'progress',
                'payload': {
                    'stage': 'completed',
                    'progress': 100,
                    'message': '项目开发完成',
                    'files_generated': self.workflow.get_generated_files()
                }
            })

            self.logger.info(f"Development completed for project {self.project_id}")

        except Exception as e:
            self.logger.error(f"Development failed: {str(e)}")
            await self.message_sender.send_message({
                'type': 'error',
                'payload': {
                    'message': f'开发过程中出现错误: {str(e)}',
                    'stage': 'error'
                }
            })
            raise

async def main():
    parser = argparse.ArgumentParser(description='AI Development Team Agent')
    parser.add_argument('--project-id', required=True, help='Project ID')
    parser.add_argument('--config', required=True, help='Project configuration JSON')
    args = parser.parse_args()

    try:
        config = json.loads(args.config)
        agent = ProjectAgent(args.project_id, config)
        await agent.start_development()
    except json.JSONDecodeError as e:
        print(json.dumps({
            'type': 'error',
            'payload': {
                'message': f'Invalid configuration JSON: {str(e)}'
            }
        }), flush=True)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            'type': 'error',
            'payload': {
                'message': f'Agent execution failed: {str(e)}'
            }
        }), flush=True)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())