# OpenPGP 中转站 API 文档

此文档描述了 OpenPGP 中转站的 API 端点，供移动应用（Android 和 iOS）使用。

## 基础 URL

所有 API 请求的基础 URL 是：

```
https://your-domain.com/
```

在开发环境中可能是：

```
http://127.0.0.1:8000/
```

## 1. 创建加密消息

### 请求

`POST /api/messages/create/`

### 请求体

```json
{
  "content": "-----BEGIN PGP MESSAGE-----\n...\n-----END PGP MESSAGE-----",
  "expiry_minutes": 60,
  "one_time_view": true,
  "note": "可选备注",
  "password": "可选密码"
}
```

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| content | string | 是 | PGP 加密的消息内容 |
| expiry_minutes | integer | 否 | 过期时间（分钟）：10、60、1440 |
| one_time_view | boolean | 否 | 是否为一次性查看 |
| note | string | 否 | 消息备注 |
| password | string | 否 | 访问密码 |

### 响应

```json
{
  "short_id": "abc123",
  "created_at": "2025-05-10T12:00:00Z",
  "url": "http://127.0.0.1:8000/m/abc123/"
}
```

## 2. 获取加密消息

### 请求

`GET /api/messages/{short_id}/`

### 响应

成功响应 (200 OK):

```json
{
  "content": "-----BEGIN PGP MESSAGE-----\n...\n-----END PGP MESSAGE-----",
  "created_at": "2025-05-10T12:00:00Z",
  "note": "可选备注",
  "one_time_view": true,
  "requires_password": false
}
```

需要密码 (403 Forbidden):

```json
{
  "detail": "需要密码验证",
  "requires_password": true
}
```

消息不存在 (404 Not Found):

```json
{
  "detail": "消息不存在或已被删除。"
}
```

消息已过期或已查看 (410 Gone):

```json
{
  "detail": "消息已过期并被删除。"
}
```

## 3. 验证消息密码

### 请求

`POST /api/messages/{short_id}/verify-password/`

### 请求体

```json
{
  "password": "访问密码"
}
```

### 响应

密码正确 (200 OK):

```json
{
  "detail": "密码验证成功。"
}
```

密码错误 (403 Forbidden):

```json
{
  "detail": "密码不正确。"
}
```

## API 使用示例

### Android (Kotlin + Retrofit)

```kotlin
// 创建消息
val message = MessageRequest(
    content = "-----BEGIN PGP MESSAGE-----\n...",
    expiryMinutes = 60,
    oneTimeView = true
)
apiService.createMessage(message).enqueue(callback)

// 获取消息
apiService.getMessage(shortId).enqueue(callback)

// 验证密码
apiService.verifyPassword(shortId, PasswordRequest("password")).enqueue(callback)
```

### iOS (Swift + URLSession)

```swift
// 创建消息
let message = [
    "content": "-----BEGIN PGP MESSAGE-----\n...",
    "expiry_minutes": 60,
    "one_time_view": true
]
apiClient.createMessage(message) { result in
    // 处理结果
}

// 获取消息
apiClient.getMessage(shortId) { result in
    // 处理结果
}

// 验证密码
apiClient.verifyPassword(shortId, password: "password") { result in
    // 处理结果
}
```

# 国际化多语言支持

## 语言切换功能

本应用支持以下语言:
- 简体中文 (zh-hans)
- 日本語 (ja)
- English (en) 
- Español (es)
- العربية (ar)

## 语言切换按钮问题排查

如果语言切换下拉菜单没有正常工作，请检查以下问题:

1. 确保已在 settings.py 中正确配置 LocaleMiddleware
2. 检查语言切换视图函数是否正确处理 POST 请求
3. 验证正在使用的是 JavaScript 文件中的 jQuery 或原生 JS 来处理表单提交
4. 在网页中检查控制台错误

## 手动创建翻译文件命令

在项目根目录 `/Users/machine/Documents/idears/gpg_message_agent` 下运行以下命令来创建翻译文件：

```bash
# 首先确保已创建locale目录
mkdir -p locale

# 然后运行翻译文件提取命令
django-admin makemessages -l zh_Hans -l ja -l en -l es -l ar

# 编辑翻译文件后，编译翻译
django-admin compilemessages
```