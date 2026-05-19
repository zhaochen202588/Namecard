"""
飞书纪要转方案 - 主程序

使用方法:
    python main.py <会议纪要来源> [选项]

示例:
    # 处理妙记链接
    python main.py "https://meetings.feishu.cn/minutes/abc123" --url
    
    # 处理 docx 文件
    python main.py "/path/to/meeting.docx" --docx
    
    # 处理文本内容
    python main.py "会议纪要文本内容..."
    
    # 指定 API Token
    python main.py "https://meetings.feishu.cn/minutes/abc123" --url --token "your_token"
"""

import argparse
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from parser import parse_minutes, MeetingMinutes
from pdf_generator import generate_plan_pdf
from feishu_sender import send_plan


def main():
    parser = argparse.ArgumentParser(
        description='将飞书会议纪要转换为执行方案 PDF 并发送',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python main.py "https://meetings.feishu.cn/minutes/abc123" --url
  python main.py "/path/to/meeting.docx" --docx
  python main.py "会议纪要文本内容..."
        '''
    )
    
    parser.add_argument(
        'source',
        help='会议纪要来源（URL、文件路径或文本内容）'
    )
    
    parser.add_argument(
        '--url',
        action='store_true',
        help='指定来源为妙记链接'
    )
    
    parser.add_argument(
        '--docx',
        action='store_true',
        help='指定来源为 docx 文件'
    )
    
    parser.add_argument(
        '--token',
        help='飞书 API Token（用于获取妙记内容）'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        default='/tmp',
        help='PDF 输出目录（默认: /tmp）'
    )
    
    parser.add_argument(
        '--no-send',
        action='store_true',
        help='只生成 PDF，不发送'
    )
    
    parser.add_argument(
        '--message',
        '-m',
        default='请查收本次会议的执行方案',
        help='发送时附带的消息'
    )
    
    args = parser.parse_args()
    
    try:
        # 1. 解析会议纪要
        print("=" * 50)
        print("步骤 1: 解析会议纪要")
        print("=" * 50)
        
        minutes = parse_minutes(
            source=args.source,
            is_url=args.url,
            is_docx=args.docx,
            api_token=args.token
        )
        
        print(f"✓ 会议主题: {minutes.title}")
        print(f"✓ 会议时间: {minutes.date or '未识别'}")
        print(f"✓ 参会人: {len(minutes.attendees)} 人")
        print(f"✓ 关键结论: {len(minutes.conclusions)} 条")
        print(f"✓ 行动项: {len(minutes.action_items)} 条")
        
        # 2. 生成 PDF
        print("\n" + "=" * 50)
        print("步骤 2: 生成执行方案 PDF")
        print("=" * 50)
        
        pdf_path = generate_plan_pdf(minutes, args.output)
        print(f"✓ PDF 已生成: {pdf_path}")
        
        # 3. 发送给相关人员
        if not args.no_send:
            print("\n" + "=" * 50)
            print("步骤 3: 发送给相关人员")
            print("=" * 50)
            
            results = send_plan(minutes, pdf_path, args.message)
            
            success_count = sum(1 for r in results if r.success)
            fail_count = len(results) - success_count
            
            print(f"\n发送完成: {success_count} 成功, {fail_count} 失败")
            
            if fail_count > 0:
                print("\n失败详情:")
                for result in results:
                    if not result.success:
                        print(f"  - {result.recipient}: {result.error}")
        else:
            print("\n✓ 已跳过发送步骤（--no-send 模式）")
        
        print("\n" + "=" * 50)
        print("处理完成！")
        print("=" * 50)
        
        return 0
        
    except ImportError as e:
        print(f"错误: 缺少必要的依赖 - {e}")
        print("\n请安装依赖:")
        print("  pip install python-docx reportlab requests")
        return 1
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
