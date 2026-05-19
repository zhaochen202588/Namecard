"""
执行方案 PDF 生成模块
生成标准结构的执行方案 PDF
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    ListFlowable, ListItem, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

from parser import MeetingMinutes, ActionItem


class PDFGenerator:
    """PDF 生成器"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_fonts()
        self._setup_custom_styles()
    
    def _setup_fonts(self):
        """设置中文字体"""
        # 尝试注册中文字体
        font_paths = [
            # Linux 常见中文字体
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            # macOS
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            # Windows
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/simsun.ttc',
            'C:/Windows/Fonts/msyh.ttc',
        ]
        
        self.chinese_font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font_name = 'ChineseFont'
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    self.chinese_font = font_name
                    break
                except:
                    continue
        
        if not self.chinese_font:
            # 如果没有找到中文字体，使用默认字体并警告
            print("警告：未找到中文字体，PDF 中的中文可能显示异常")
            self.chinese_font = 'Helvetica'
    
    def _setup_custom_styles(self):
        """设置自定义样式"""
        # 标题样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontName=self.chinese_font,
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=30,
        )
        
        # 章节标题样式
        self.section_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading2'],
            fontName=self.chinese_font,
            fontSize=16,
            leading=22,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#1a1a1a'),
        )
        
        # 正文样式
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontName=self.chinese_font,
            fontSize=11,
            leading=18,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        )
        
        # 列表项样式
        self.list_style = ParagraphStyle(
            'ListItem',
            parent=self.styles['BodyText'],
            fontName=self.chinese_font,
            fontSize=11,
            leading=16,
            leftIndent=20,
            spaceAfter=6,
        )
        
        # 信息标签样式
        self.label_style = ParagraphStyle(
            'Label',
            parent=self.styles['BodyText'],
            fontName=self.chinese_font,
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#666666'),
        )
        
        # 信息值样式
        self.value_style = ParagraphStyle(
            'Value',
            parent=self.styles['BodyText'],
            fontName=self.chinese_font,
            fontSize=11,
            leading=14,
        )
    
    def generate(self, minutes: MeetingMinutes, output_path: str) -> str:
        """
        生成执行方案 PDF
        
        Args:
            minutes: 会议纪要数据
            output_path: 输出 PDF 路径
            
        Returns:
            生成的 PDF 文件路径
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )
        
        story = []
        
        # 1. 标题
        story.append(Paragraph("执行方案", self.title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # 2. 背景信息
        story.append(Paragraph("一、背景", self.section_style))
        story.extend(self._build_background(minutes))
        story.append(Spacer(1, 0.3*cm))
        
        # 3. 关键结论
        story.append(Paragraph("二、关键结论", self.section_style))
        story.extend(self._build_conclusions(minutes.conclusions))
        story.append(Spacer(1, 0.3*cm))
        
        # 4. 行动项清单
        story.append(Paragraph("三、行动项清单", self.section_style))
        story.extend(self._build_action_items(minutes.action_items))
        story.append(Spacer(1, 0.3*cm))
        
        # 5. 时间线
        story.append(Paragraph("四、时间线", self.section_style))
        story.extend(self._build_timeline(minutes.action_items))
        
        # 生成 PDF
        doc.build(story)
        
        return output_path
    
    def _build_background(self, minutes: MeetingMinutes) -> List:
        """构建背景信息部分"""
        elements = []
        
        # 会议主题
        if minutes.title:
            elements.append(Paragraph(f"<b>会议主题：</b>{minutes.title}", self.body_style))
        
        # 会议时间
        if minutes.date:
            elements.append(Paragraph(f"<b>会议时间：</b>{minutes.date}", self.body_style))
        
        # 参会人
        if minutes.attendees:
            attendees_str = '、'.join(minutes.attendees[:10])  # 最多显示10人
            if len(minutes.attendees) > 10:
                attendees_str += f" 等 {len(minutes.attendees)} 人"
            elements.append(Paragraph(f"<b>参会人：</b>{attendees_str}", self.body_style))
        
        # 生成时间
        elements.append(Paragraph(
            f"<b>方案生成时间：</b>{datetime.now().strftime('%Y年%m月%d日 %H:%M')}",
            self.body_style
        ))
        
        return elements
    
    def _build_conclusions(self, conclusions: List[str]) -> List:
        """构建关键结论部分"""
        elements = []
        
        if not conclusions:
            elements.append(Paragraph("暂无明确结论", self.body_style))
            return elements
        
        for i, conclusion in enumerate(conclusions, 1):
            # 转义 HTML 特殊字符
            conclusion = conclusion.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elements.append(Paragraph(f"{i}. {conclusion}", self.list_style))
        
        return elements
    
    def _build_action_items(self, action_items: List[ActionItem]) -> List:
        """构建行动项清单表格"""
        elements = []
        
        # 过滤掉没有负责人的行动项
        valid_items = [item for item in action_items if item.has_assignee()]
        
        if not valid_items:
            elements.append(Paragraph("暂无明确负责人的行动项", self.body_style))
            return elements
        
        # 创建表格数据
        table_data = [['序号', '行动项', '负责人', '截止时间']]
        
        for i, item in enumerate(valid_items, 1):
            # 转义 HTML 特殊字符
            content = item.content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            assignee = (item.assignee or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            deadline = (item.deadline or '待定').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            table_data.append([
                str(i),
                Paragraph(content, self.body_style),
                assignee,
                deadline
            ])
        
        # 创建表格
        table = Table(table_data, colWidths=[1*cm, 8*cm, 2.5*cm, 2.5*cm])
        
        # 设置表格样式
        table_style = TableStyle([
            # 表头样式
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5C8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.chinese_font),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # 数据行样式
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), self.chinese_font),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (3, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            
            # 网格线
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#2E5C8A')),
            
            # 行高
            ('ROWHEIGHT', (0, 0), (-1, -1), 30),
        ])
        
        # 交替行背景色
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F5F5F5'))
        
        table.setStyle(table_style)
        elements.append(table)
        
        return elements
    
    def _build_timeline(self, action_items: List[ActionItem]) -> List:
        """构建时间线部分"""
        elements = []
        
        # 过滤有截止日期的行动项
        items_with_deadline = [
            item for item in action_items 
            if item.has_assignee() and item.deadline
        ]
        
        if not items_with_deadline:
            elements.append(Paragraph("暂无明确的截止时间", self.body_style))
            return elements
        
        # 按截止日期排序（简化处理，仅按字符串排序）
        sorted_items = sorted(items_with_deadline, key=lambda x: x.deadline or '')
        
        # 创建时间线表格
        table_data = [['时间', '事项', '负责人']]
        
        for item in sorted_items:
            content = item.content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            assignee = item.assignee.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            table_data.append([
                item.deadline,
                Paragraph(content[:50] + ('...' if len(content) > 50 else ''), self.body_style),
                assignee
            ])
        
        table = Table(table_data, colWidths=[3*cm, 8*cm, 3*cm])
        
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A90A4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.chinese_font),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            
            ('FONTNAME', (0, 1), (-1, -1), self.chinese_font),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#4A90A4')),
        ])
        
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F0F7FA'))
        
        table.setStyle(table_style)
        elements.append(table)
        
        return elements


def generate_plan_pdf(minutes: MeetingMinutes, output_dir: str = "/tmp") -> str:
    """
    生成执行方案 PDF 的便捷函数
    
    Args:
        minutes: 会议纪要数据
        output_dir: 输出目录
        
    Returns:
        生成的 PDF 文件路径
    """
    generator = PDFGenerator()
    
    # 生成文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_title = ''.join(c for c in minutes.title if c.isalnum() or c in '_-')[:20]
    filename = f"执行方案_{safe_title}_{timestamp}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    return generator.generate(minutes, output_path)
