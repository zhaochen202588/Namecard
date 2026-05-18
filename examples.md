# 使用示例

## 示例 1：完整信息

**用户输入：**
```
帮我做一个个人名片，我叫张三，简介是"全栈开发者 | 技术博主"，
我的个人网站是 https://zhangsan.dev，
视频号是 https://channels.weixin.qq.com/zhangsan，
小红书是 https://www.xiaohongshu.com/user/profile/12345
```

**执行结果：**
- 生成 `personal_card.jpg` - 名片图片
- 生成 `personal_card.html` - 可点击跳转的网页名片

---

## 示例 2：部分信息

**用户输入：**
```
帮我做一个名片，我叫李四，只要放我的小红书：https://www.xiaohongshu.com/user/profile/67890
```

**执行结果：**
- 生成名片，只显示小红书按钮
- 其他链接使用占位符或隐藏

---

## 示例 3：使用占位符

**用户输入：**
```
帮我做一个名片模板，我还没想好具体信息
```

**执行结果：**
- 生成带占位符的名片
- 告知用户可以在 HTML 中替换以下内容：
  - `您的名字` → 真实名字
  - `个人简介 | 创作者` → 个人简介
  - 各链接占位符 → 真实链接

---

## 后续自定义

用户可以编辑 HTML 文件进一步自定义：

1. **修改颜色**：编辑 `.link-btn.website`、`.link-btn.video`、`.link-btn.xiaohongshu` 的 `background` 属性

2. **添加更多链接**：复制 `.link-btn` 代码块，修改图标和链接

3. **修改头像**：将 `<img src="{{AVATAR_URL}}">` 中的 URL 替换为实际头像地址

4. **部署到网上**：
   - GitHub Pages: 推送到仓库，开启 Pages
   - Vercel/Netlify: 直接拖拽上传
   - 个人服务器: 上传 HTML 文件
