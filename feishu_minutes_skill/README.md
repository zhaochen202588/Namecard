# 飞书纪要转方案

将飞书会议纪要（妙记链接或导出的 docx）自动提炼为执行方案 PDF，并通过飞书 CLI 私聊发送给参会人及行动项负责人。

## 功能特性

- 📄 **智能解析**：支持飞书妙记链接和 docx 文件
- 📝 **内容提炼**：自动提取关键结论、决策和行动项
- 📊 **PDF 生成**：生成标准结构的执行方案文档
- 📤 **自动分发**：通过飞书 CLI 私聊发送给相关人员

## 执行方案 PDF 结构

1. **背景**：会议基本信息（时间、参会人、议题）
2. **关键结论**：会议达成的核心结论和决策
3. **行动项清单**：具体待办事项、负责人、截止时间
4. **时间线**：关键里程碑和时间节点

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装飞书 CLI

参考官方文档：https://open.feishu.cn/document/tools/cli/overview

```bash
# macOS
brew install feishu-cli

# 或通过 npm
npm install -g @larksuite/cli
```

### 3. 配置飞书 CLI

```bash
feishu login
```

## 使用方法

### 命令行

```bash
# 处理妙记链接
python main.py "https://meetings.feishu.cn/minutes/abc123" --url

# 处理 docx 文件
python main.py "/path/to/meeting.docx" --docx

# 处理文本内容
python main.py "会议纪要文本内容..."

# 指定 API Token（用于获取妙记内容）
python main.py "https://meetings.feishu.cn/minutes/abc123" --url --token "your_token"

# 只生成 PDF，不发送
python main.py "/path/to/meeting.docx" --docx --no-send

# 指定输出目录
python main.py "/path/to/meeting.docx" --docx --output "/path/to/output"

# 自定义发送消息
python main.py "/path/to/meeting.docx" --docx --message "请查收本次会议的执行方案"
```

### 作为模块使用

```python
from modules.parser import parse_minutes
from modules.pdf_generator import generate_plan_pdf
from modules.feishu_sender import send_plan

# 解析会议纪要
minutes = parse_minutes(
    source="/path/to/meeting.docx",
    is_docx=True
)

# 生成 PDF
pdf_path = generate_plan_pdf(minutes, "/tmp")

# 发送给相关人员
results = send_plan(minutes, pdf_path)
```

## 发送规则

- **发送对象**：参会人 + 行动项中被@的人
- **发送方式**：私聊，附带简短说明文字
- **无明确负责人的行动项**：跳过不处理

## 项目结构

```
feishu-minutes-skill/
├── SKILL.md              # Skill 定义文件
├── README.md             # 项目说明
├── requirements.txt      # Python 依赖
├── main.py              # 主程序入口
└── modules/
    ├── parser.py        # 纪要解析模块
    ├── pdf_generator.py # PDF 生成模块
    └── feishu_sender.py # 飞书发送模块
```

## 依赖要求

- Python 3.8+
- 飞书 CLI 已安装并配置
- 具有发送消息的权限

## 注意事项

1. **飞书 CLI 权限**：确保飞书 CLI 已登录且具有发送消息的权限
2. **用户查找**：发送前会自动搜索用户，如果找不到会跳过
3. **文件大小**：PDF 文件大小限制请参考飞书官方文档
4. **中文字体**：PDF 生成需要系统中安装中文字体

## 常见问题

### Q: 无法找到飞书 CLI
A: 请确保飞书 CLI 已安装并添加到 PATH 环境变量

### Q: 发送消息失败
A: 检查飞书 CLI 是否已登录：`feishu login`

### Q: PDF 中文显示异常
A: 请安装中文字体，如文泉驿微米黑、Noto Sans CJK 等

## License

MIT
