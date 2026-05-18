# Personal Card Skill - 执行指令

当用户请求创建个人名片时，请按照以下步骤执行：

## 1. 收集信息

首先检查用户是否已提供以下信息，如果没有，使用 AskUserQuestion 工具询问：

- **名字** (必填): 名片上显示的名字
- **简介** (可选): 一句话介绍
- **头像** (可选): 头像图片
- **个人网址** (可选): 个人网站链接
- **视频号链接** (可选): 微信视频号地址
- **小红书链接** (可选): 小红书主页地址

如果用户暂时没有信息，使用占位符，告知用户后续可以替换。

## 2. 生成图片版名片

使用 GenerateImage 工具，prompt 如下：

```
PURPOSE: A professional personal digital business card image, similar to WeChat official account card style.

DESIGN DETAILS:
- Clean, modern, minimalist white card design with rounded corners and subtle shadow
- Left side: circular avatar area (with person silhouette icon if no avatar)
- Right side: Name in bold black Chinese characters
- Below name: Brief description in gray text
- Bottom section: Three rounded rectangular buttons:
  1. Globe icon + "个人网址" (blue)
  2. Video play icon + "视频号" (red)
  3. Heart icon + "小红书" (orange)
- Background: light gradient from white to very light gray
- Professional, elegant, Chinese-friendly typography
```

保存路径: `/workspace/personal_card.jpg`

## 3. 生成网页版名片

读取模板文件 `template.html`，替换以下占位符：

| 占位符 | 替换为 |
|--------|--------|
| `{{NAME}}` | 用户名字 |
| `{{BIO}}` | 个人简介 |
| `{{AVATAR_URL}}` | 头像URL（为空则显示默认图标） |
| `{{WEBSITE_URL}}` | 个人网址 |
| `{{VIDEO_URL}}` | 视频号链接 |
| `{{XIAOHONGSHU_URL}}` | 小红书链接 |

保存路径: `/workspace/personal_card.html`

## 4. 输出结果

向用户提供文件链接：

```
名片已生成！

📄 [查看图片版名片](computer:///workspace/personal_card.jpg)
🌐 [查看网页版名片](computer:///workspace/personal_card.html)

网页版名片点击按钮即可跳转到对应平台。
```

## 注意事项

- 如果用户只提供部分链接，只显示对应的按钮（可修改 HTML 移除不需要的链接）
- 图片版是静态的，仅供展示和分享
- 网页版是可交互的，支持点击跳转
- 建议用户将网页部署到自己的服务器或使用 GitHub Pages 托管
