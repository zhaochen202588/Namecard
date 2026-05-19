"""
飞书 CLI 消息发送模块
通过飞书 CLI 私聊发送 PDF 附件
"""

import subprocess
import json
import os
from typing import List, Optional
from dataclasses import dataclass

from parser import MeetingMinutes, ActionItem


@dataclass
class SendResult:
    """发送结果"""
    success: bool
    recipient: str
    message: str
    error: Optional[str] = None


class FeishuCLI:
    """飞书 CLI 封装"""
    
    def __init__(self):
        self._check_cli()
    
    def _check_cli(self):
        """检查飞书 CLI 是否已安装"""
        try:
            result = subprocess.run(
                ['feishu', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                raise RuntimeError("飞书 CLI 未正确安装或配置")
        except FileNotFoundError:
            raise RuntimeError(
                "未找到飞书 CLI 命令。请确保已安装飞书 CLI 并添加到 PATH。\n"
                "安装指南：https://open.feishu.cn/document/tools/cli/overview"
            )
    
    def _run_command(self, args: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
        """
        运行飞书 CLI 命令
        
        Args:
            args: 命令参数
            timeout: 超时时间（秒）
            
        Returns:
            命令执行结果
        """
        cmd = ['feishu'] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result
    
    def search_user(self, keyword: str) -> List[dict]:
        """
        搜索用户
        
        Args:
            keyword: 搜索关键词（姓名、邮箱等）
            
        Returns:
            用户列表
        """
        result = self._run_command(['search', 'user', keyword])
        
        if result.returncode != 0:
            print(f"搜索用户失败: {result.stderr}")
            return []
        
        try:
            # 解析输出
            output = result.stdout.strip()
            # 飞书 CLI 输出可能是 JSON 或表格格式，这里尝试解析 JSON
            if output.startswith('[') or output.startswith('{'):
                data = json.loads(output)
                return data if isinstance(data, list) else [data]
            else:
                # 表格格式，需要手动解析
                return self._parse_table_output(output)
        except json.JSONDecodeError:
            return self._parse_table_output(result.stdout)
    
    def _parse_table_output(self, output: str) -> List[dict]:
        """解析表格格式的输出"""
        lines = output.strip().split('\n')
        users = []
        
        # 找到表头和数据分隔线
        header_idx = -1
        for i, line in enumerate(lines):
            if '---' in line or '===' in line:
                header_idx = i - 1
                break
        
        if header_idx < 0:
            return []
        
        # 解析表头
        headers = [h.strip() for h in lines[header_idx].split('|') if h.strip()]
        
        # 解析数据行
        for line in lines[header_idx + 2:]:
            if not line.strip() or '---' in line:
                continue
            
            values = [v.strip() for v in line.split('|') if v.strip()]
            if len(values) >= len(headers):
                user = dict(zip(headers, values))
                users.append(user)
        
        return users
    
    def get_user_id(self, name_or_email: str) -> Optional[str]:
        """
        获取用户 ID
        
        Args:
            name_or_email: 用户姓名或邮箱
            
        Returns:
            用户 ID（open_id 或 user_id）
        """
        users = self.search_user(name_or_email)
        
        if not users:
            return None
        
        # 优先返回完全匹配的用户
        for user in users:
            if user.get('name') == name_or_email or user.get('email') == name_or_email:
                return user.get('open_id') or user.get('user_id')
        
        # 返回第一个搜索结果
        return users[0].get('open_id') or users[0].get('user_id')
    
    def send_message_with_file(
        self,
        user_id: str,
        file_path: str,
        message: str = "请查收会议纪要执行方案"
    ) -> SendResult:
        """
        发送文件消息
        
        Args:
            user_id: 用户 ID
            file_path: 文件路径
            message: 附带消息
            
        Returns:
            发送结果
        """
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return SendResult(
                success=False,
                recipient=user_id,
                message=message,
                error=f"文件不存在: {file_path}"
            )
        
        # 使用飞书 CLI 发送文件
        # 注意：飞书 CLI 的具体命令格式可能需要根据实际版本调整
        result = self._run_command([
            'message',
            'send',
            '--user_id', user_id,
            '--content', message,
            '--file', file_path
        ])
        
        if result.returncode == 0:
            return SendResult(
                success=True,
                recipient=user_id,
                message=message
            )
        else:
            return SendResult(
                success=False,
                recipient=user_id,
                message=message,
                error=result.stderr
            )
    
    def send_to_chat(
        self,
        chat_id: str,
        file_path: str,
        message: str = "请查收会议纪要执行方案"
    ) -> SendResult:
        """
        发送到群聊
        
        Args:
            chat_id: 群聊 ID
            file_path: 文件路径
            message: 附带消息
            
        Returns:
            发送结果
        """
        if not os.path.exists(file_path):
            return SendResult(
                success=False,
                recipient=chat_id,
                message=message,
                error=f"文件不存在: {file_path}"
            )
        
        result = self._run_command([
            'message',
            'send',
            '--chat_id', chat_id,
            '--content', message,
            '--file', file_path
        ])
        
        if result.returncode == 0:
            return SendResult(
                success=True,
                recipient=chat_id,
                message=message
            )
        else:
            return SendResult(
                success=False,
                recipient=chat_id,
                message=message,
                error=result.stderr
            )


class PlanDistributor:
    """执行方案分发器"""
    
    def __init__(self):
        self.cli = FeishuCLI()
    
    def get_recipients(self, minutes: MeetingMinutes) -> List[str]:
        """
        获取发送对象列表
        
        发送对象包括：
        1. 参会人
        2. 行动项中有明确负责人的
        
        Args:
            minutes: 会议纪要
            
        Returns:
            收件人列表（姓名/邮箱）
        """
        recipients = set()
        
        # 添加参会人
        for attendee in minutes.attendees:
            if attendee and attendee.strip():
                recipients.add(attendee.strip())
        
        # 添加行动项负责人（只添加有明确负责人的）
        for item in minutes.action_items:
            if item.has_assignee():
                recipients.add(item.assignee.strip())
        
        return list(recipients)
    
    def distribute(
        self,
        minutes: MeetingMinutes,
        pdf_path: str,
        message: str = "请查收本次会议的执行方案"
    ) -> List[SendResult]:
        """
        分发执行方案
        
        Args:
            minutes: 会议纪要
            pdf_path: PDF 文件路径
            message: 附带消息
            
        Returns:
            发送结果列表
        """
        results = []
        recipients = self.get_recipients(minutes)
        
        if not recipients:
            print("警告：没有找到收件人")
            return results
        
        print(f"准备发送给 {len(recipients)} 位收件人: {', '.join(recipients)}")
        
        for recipient in recipients:
            # 获取用户 ID
            user_id = self.cli.get_user_id(recipient)
            
            if not user_id:
                results.append(SendResult(
                    success=False,
                    recipient=recipient,
                    message=message,
                    error=f"无法找到用户: {recipient}"
                ))
                continue
            
            # 发送消息
            result = self.cli.send_message_with_file(user_id, pdf_path, message)
            results.append(result)
            
            if result.success:
                print(f"✓ 已发送给 {recipient}")
            else:
                print(f"✗ 发送给 {recipient} 失败: {result.error}")
        
        return results
    
    def distribute_to_users(
        self,
        user_ids: List[str],
        pdf_path: str,
        message: str = "请查收本次会议的执行方案"
    ) -> List[SendResult]:
        """
        直接指定用户 ID 发送
        
        Args:
            user_ids: 用户 ID 列表
            pdf_path: PDF 文件路径
            message: 附带消息
            
        Returns:
            发送结果列表
        """
        results = []
        
        for user_id in user_ids:
            result = self.cli.send_message_with_file(user_id, pdf_path, message)
            results.append(result)
            
            if result.success:
                print(f"✓ 已发送给 {user_id}")
            else:
                print(f"✗ 发送给 {user_id} 失败: {result.error}")
        
        return results


def send_plan(
    minutes: MeetingMinutes,
    pdf_path: str,
    message: str = "请查收本次会议的执行方案"
) -> List[SendResult]:
    """
    发送执行方案的便捷函数
    
    Args:
        minutes: 会议纪要
        pdf_path: PDF 文件路径
        message: 附带消息
        
    Returns:
        发送结果列表
    """
    distributor = PlanDistributor()
    return distributor.distribute(minutes, pdf_path, message)
