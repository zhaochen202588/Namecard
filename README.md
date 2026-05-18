# Personal Card Skill - 个人名片生成器

## 简介

这是一个用于生成个人数字名片的 SOLO skill。可以创建类似微信"公众号名片"风格的精美名片，支持添加个人网址、视频号、小红书等链接，别人点击即可跳转。

## 功能特点

- 🎨 生成精美的名片图片（PNG/JPG）
- 🌐 生成交互式网页名片（HTML），支持点击跳转
- 📱 类似微信名片风格，简洁优雅
- 🔗 支持多个平台链接：个人网址、视频号、小红书
- ✏️ 支持自定义头像、名字、简介

## 使用方法

### 触发条件

当用户说以下内容时，自动加载此 skill：
- "帮我做一个个人名片"
- "生成一个名片"
- "我想做一个带链接的名片"
- "制作数字名片"

### 执行步骤

#### 步骤 1：收集用户信息

询问用户以下信息（如果用户尚未提供）：

1. **名字**：名片上显示的名字
2. **简介**：一句话介绍（可选）
3. **头像**：头像图片（可选，可后续替换）
4. **个人网址**：用户的个人网站链接
5. **视频号链接**：微信视频号地址
6. **小红书链接**：小红书个人主页地址

如果用户暂时没有信息，使用占位符，后续替换。

#### 步骤 2：生成图片版名片

使用 `GenerateImage` 工具生成名片图片：

```
prompt: A professional personal digital business card image, similar to WeChat official account card style.
- Clean, modern, minimalist white card design with rounded corners
- Left side: circular avatar area
- Right side: Name in bold, brief description below
- Bottom: Three rounded buttons for links (Website, Video Account, Xiaohongshu)
- Chinese-friendly typography
```

保存到：`/workspace/personal_card.jpg`

#### 步骤 3：生成网页版名片

创建 HTML 文件，包含：
- 响应式设计，适配手机和电脑
- 三个可点击的链接按钮
- 精美的渐变色彩和动画效果
- 悬停交互效果

保存到：`/workspace/personal_card.html`

#### 步骤 4：输出结果

向用户提供两个文件的链接：
- 图片版：`computer:///workspace/personal_card.jpg`
- 网页版：`computer:///workspace/personal_card.html`

## 输出文件

| 文件 | 说明 |
|------|------|
| `personal_card.jpg` | 名片图片，可直接分享 |
| `personal_card.html` | 网页名片，点击链接可跳转 |

## 自定义替换

用户可以在 HTML 文件中搜索以下占位符进行替换：

| 占位符 | 替换为 |
|--------|--------|
| `您的名字` | 真实名字 |
| `个人简介 | 创作者` | 个人简介 |
| `👤` | 头像图片路径 |
| `https://yourwebsite.com` | 个人网址 |
| `https://channels.weixin.qq.com/yourchannel` | 视频号链接 |
| `https://www.xiaohongshu.com/user/profile/yourid` | 小红书链接 |

## 示例对话

**用户**：帮我做一个个人名片，我想放我的视频号和小红书链接

**SOLO**：好的！我来帮您制作个人名片。请问：
1. 您的名字是？
2. 您的视频号链接是？
3. 您的小红书主页链接是？

**用户**：我叫张三，视频号是 xxx，小红书是 yyy

**SOLO**：[生成名片文件]

名片已生成！
- [查看图片版名片](computer:///workspace/personal_card.jpg)
- [查看网页版名片](computer:///workspace/personal_card.html)

## 技术说明

- 图片生成：使用 AI 图像生成工具
- 网页设计：纯 HTML + CSS，无需 JavaScript 框架
- 响应式：支持手机和桌面端显示
- 交互效果：CSS hover 动画，点击跳转

## 版本

- v1.0 - 初始版本，支持基本名片生成功能
