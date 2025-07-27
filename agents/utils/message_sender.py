import json
import sys
from typing import Dict, Any

class MessageSender:
    """消息发送器，用于向Node.js后端发送消息"""
    
    async def send_message(self, data: Dict[str, Any]) -> None:
        """发送消息到Node.js后端"""
        try:
            message = json.dumps(data, ensure_ascii=False)
            print(message, flush=True)
        except Exception as e:
            # 发生错误时，发送错误消息
            error_message = {
                'type': 'error',
                'payload': {
                    'message': f'消息发送失败: {str(e)}'
                }
            }
            print(json.dumps(error_message), flush=True)