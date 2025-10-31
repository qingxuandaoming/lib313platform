# 313实验室开放平台 API 文档

## 概述

313实验室开放平台提供了完整的RESTful API，用于管理实验室的成员、项目、分享会、设备、值日安排和文档等功能。

## 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **认证方式**: Bearer Token (待实现)
- **数据格式**: JSON
- **字符编码**: UTF-8

## 通用响应格式

## 通用响应格式说明

### 成功响应

```json

### 成功响应
```json
{
  "data": [...],
  "total": 100,
  "message": "操作成功"
}
```

### 错误响应

```json
{
  "detail": "错误信息",
  "status_code": 400
}
```

## API 接口

### 1. 成员管理 (Members)

#### 1.1 获取成员列表

- **URL**: `GET /members`
- **参数**:
  - `skip` (int, optional): 跳过的记录数，默认0
  - `limit` (int, optional): 返回的记录数，默认100
  - `search` (string, optional): 搜索关键词（姓名或学号）
  - `role` (string, optional): 角色筛选 (leader/member/alumni)
  - `grade` (int, optional): 年级筛选

**响应示例**:

- **URL**: `GET /members`
- **参数**:
  - `skip` (int, optional): 跳过的记录数，默认0
  - `limit` (int, optional): 返回的记录数，默认100
  - `search` (string, optional): 搜索关键词（姓名或学号）
  - `role` (string, optional): 角色筛选 (leader/member/alumni)
  - `grade` (int, optional): 年级筛选

**响应示例**:

```json

{
  "data": [
    {
      "id": 1,
      "name": "张三",
      "student_id": "2021001",
      "grade": 2021,
      "major": "计算机科学与技术",
      "role": "member",
      "email": "zhangsan@example.com",
      "phone": "13800138000",
      "github": "zhangsan",
      "bio": "热爱编程的学生",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### 1.2 获取单个成员

- **URL**: `GET /members/{member_id}`
- **参数**:
  
  - `member_id` (int): 成员ID

#### 1.3 创建成员

- **URL**: `POST /members`
- **请求体**:
  
```json

{
  "name": "张三",
  "student_id": "2021001",
  "grade": 2021,
  "major": "计算机科学与技术",
  "role": "member",
  "email": "zhangsan@example.com",
  "phone": "13800138000",
  "github": "zhangsan",
  "bio": "热爱编程的学生"
}
```

#### 1.4 更新成员

- **URL**: `PUT /members/{member_id}`
- **请求体**: 同创建成员，所有字段可选

#### 1.5 删除成员

- **URL**: `DELETE /members/{member_id}`

### 2. 项目管理 (Projects)

#### 2.1 获取项目列表

- **URL**: `GET /projects`
- **参数**:
  - `skip` (int, optional): 跳过的记录数
  - `limit` (int, optional): 返回的记录数
  - `search` (string, optional): 搜索关键词
  - `status` (string, optional): 状态筛选 (planning/in_progress/completed/archived)
  - `leader_id` (int, optional): 负责人ID筛选

**响应示例**:

```json

{
  "data": [
    {
      "id": 1,
      "name": "智能聊天机器人",
      "description": "基于深度学习的智能对话系统",
      "status": "in_progress",
      "leader_id": 1,
      "leader": {
        "id": 1,
        "name": "张三"
      },
      "start_date": "2024-01-01T00:00:00Z",
      "end_date": "2024-06-01T00:00:00Z",
      "github_url": "https://github.com/313lab/chatbot",
      "demo_url": "https://demo.313lab.com/chatbot",
      "tags": "AI,Python,深度学习",
      "members": [
        {
          "id": 1,
          "name": "张三",
          "role": "leader"
        }
      ],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### 2.2 获取单个项目

- **URL**: `GET /projects/{project_id}`

#### 2.3 创建项目

- **URL**: `POST /projects`

- **请求体**:
  
```json
{
  "name": "智能聊天机器人",
  "description": "基于深度学习的智能对话系统",
  "status": "planning",
  "leader_id": 1,
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-06-01T00:00:00Z",
  "github_url": "https://github.com/313lab/chatbot",
  "demo_url": "https://demo.313lab.com/chatbot",
  "tags": "AI,Python,深度学习",
  "member_ids": [1, 2, 3]
}
```

#### 2.4 更新项目

- **URL**: `PUT /projects/{project_id}`

#### 2.5 删除项目

- **URL**: `DELETE /projects/{project_id}`

#### 2.6 添加项目成员

- **URL**: `POST /projects/{project_id}/members`
- **请求体**:
  
```json
{
  "member_id": 2,
  "role": "member"
}
```

#### 2.7 移除项目成员

- **URL**: `DELETE /projects/{project_id}/members/{member_id}`

### 3. 分享会管理 (Sessions)

#### 3.1 获取分享会列表

- **URL**: `GET /sessions`
- **参数**:
  - `skip` (int, optional): 跳过的记录数
  - `limit` (int, optional): 返回的记录数
  - `semester` (string, optional): 学期筛选
  - `speaker_id` (int, optional): 分享者ID筛选

#### 3.2 获取单个分享会

- **URL**: `GET /sessions/{session_id}`

#### 3.3 创建分享会

- **URL**: `POST /sessions`
- **请求体**:
  
```json
{
  "session_number": 1,
  "semester": "2024春",
  "title": "深度学习入门",
  "speaker_id": 1,
  "session_date": "2024-03-15T14:00:00Z",
  "location": "实验室",
  "description": "介绍深度学习的基本概念和应用"
}
```

#### 3.4 更新分享会

- **URL**: `PUT /sessions/{session_id}`

#### 3.5 删除分享会

- **URL**: `DELETE /sessions/{session_id}`

### 4. 设备管理 (Devices)

#### 4.1 获取设备列表

- **URL**: `GET /devices`
- **参数**:
  - `skip` (int, optional): 跳过的记录数
  - `limit` (int, optional): 返回的记录数
  - `device_type` (string, optional): 设备类型筛选
  - `status` (string, optional): 状态筛选 (available/in_use/maintenance/retired)

#### 4.2 获取单个设备

- **URL**: `GET /devices/{device_id}`

#### 4.3 创建设备

- **URL**: `POST /devices`
- **请求体**:
  
```json
{
  "name": "MacBook Pro",
  "device_type": "laptop",
  "brand": "Apple",
  "model": "MacBook Pro 16-inch",
  "serial_number": "ABC123456",
  "specifications": "M1 Pro, 16GB RAM, 512GB SSD",
  "status": "available",
  "current_user_id": null
}
```

#### 4.4 更新设备

- **URL**: `PUT /devices/{device_id}`

#### 4.5 删除设备

- **URL**: `DELETE /devices/{device_id}`

### 5. 首页统计 (Stats)

#### 5.1 获取首页统计

- **URL**: `GET /stats`

**响应示例**:

```json
{
  "projects": 12,
  "members": 25,
  "sessions": 13,
  "devices": 8
}
```

### 5. 值日安排 (Duty)

#### 5.1 获取值日安排列表

- **URL**: `GET /duty`
- **参数**:
  - `skip` (int, optional): 跳过的记录数
  - `limit` (int, optional): 返回的记录数
  - `week_start` (date, optional): 周开始日期筛选
  - `member_id` (int, optional): 成员ID筛选

#### 5.2 获取单个值日安排

- **URL**: `GET /duty/{duty_id}`

#### 5.3 创建值日安排

- **URL**: `POST /duty`
- **请求体**:
  
```json
{
  "member_id": 1,
  "week_start": "2024-03-11",
  "week_end": "2024-03-17",
  "tasks": "清洁实验室，整理设备",
  "status": "pending"
}
```

#### 5.4 更新值日安排

- **URL**: `PUT /duty/{duty_id}`

#### 5.5 删除值日安排

- **URL**: `DELETE /duty/{duty_id}`

### 6. 文件管理 (Files)

#### 6.1 获取文件列表

- **URL**: `GET /files`
- **参数**:
  - `skip` (int, optional): 跳过的记录数
  - `limit` (int, optional): 返回的记录数
  - `project_id` (int, optional): 项目ID筛选
  - `session_id` (int, optional): 分享会ID筛选
  - `file_type` (string, optional): 文件类型筛选 (document/image/presentation/video/other)
  - `search` (string, optional): 搜索关键词

**响应示例**:

```json
{
  "data": [
    {
      "id": 1,
      "filename": "uuid-filename.pdf",
      "original_filename": "项目文档.pdf",
      "file_path": "/uploads/projects/1/uuid-filename.pdf",
      "file_type": "document",
      "file_size": 1024000,
      "mime_type": "application/pdf",
      "project_id": 1,
      "session_id": null,
      "uploader_id": 1,
      "description": "项目需求文档",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### 6.2 获取文件统计

- **URL**: `GET /files/stats`

**响应示例**:

```json
{
  "total_files": 100,
  "total_size": 1073741824,
  "total_size_mb": 1024.0,
  "type_stats": {
    "document": 50,
    "image": 30,
    "presentation": 15,
    "video": 3,
    "other": 2
  }
}
```

#### 6.3 获取单个文件

- **URL**: `GET /files/{file_id}`

#### 6.4 下载文件

- **URL**: `GET /files/{file_id}/download`
- **响应**: 文件流

#### 6.5 上传文件

- **URL**: `POST /files/upload`
- **Content-Type**: `multipart/form-data`
- **参数**:
  - `file` (file): 要上传的文件
  - `project_id` (int, optional): 关联项目ID
  - `session_id` (int, optional): 关联分享会ID
  - `description` (string, optional): 文件描述

#### 6.6 批量上传文件

- **URL**: `POST /files/batch-upload`
- **Content-Type**: `multipart/form-data`
- **参数**:
  - `files` (file[]): 要上传的文件列表（最多10个）
  - `project_id` (int, optional): 关联项目ID
  - `session_id` (int, optional): 关联分享会ID

#### 6.7 更新文件信息

- **URL**: `PUT /files/{file_id}`
- **请求体**:
  
```json
{
  "original_filename": "新文件名.pdf",
  "description": "更新后的描述"
}
```

#### 6.8 删除文件

- **URL**: `DELETE /files/{file_id}`

## 错误码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 删除成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 413 | 文件过大 |
| 422 | 数据验证失败 |
| 500 | 服务器内部错误 |

## 数据模型

### Member (成员)

```json
{
  "id": "integer",
  "name": "string",
  "student_id": "string",
  "grade": "integer",
  "major": "string",
  "role": "string (leader/member/alumni)",
  "email": "string",
  "phone": "string",
  "github": "string",
  "bio": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Project (项目)

```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "status": "string (planning/in_progress/completed/archived)",
  "leader_id": "integer",
  "start_date": "datetime",
  "end_date": "datetime",
  "github_url": "string",
  "demo_url": "string",
  "tags": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Session (分享会)

```json
{
  "id": "integer",
  "session_number": "integer",
  "semester": "string",
  "title": "string",
  "speaker_id": "integer",
  "session_date": "datetime",
  "location": "string",
  "description": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Device (设备)

```json
{
  "id": "integer",
  "name": "string",
  "device_type": "string",
  "brand": "string",
  "model": "string",
  "serial_number": "string",
  "specifications": "string",
  "status": "string (available/in_use/maintenance/retired)",
  "current_user_id": "integer",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### File (文件)

```json
{
  "id": "integer",
  "filename": "string",
  "original_filename": "string",
  "file_path": "string",
  "file_type": "string (document/image/presentation/video/other)",
  "file_size": "integer",
  "mime_type": "string",
  "project_id": "integer",
  "session_id": "integer",
  "uploader_id": "integer",
  "description": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 使用示例

### JavaScript/Axios 示例

```javascript
// 获取成员列表
const getMembers = async () => {
  try {
    const response = await axios.get('/api/v1/members', {
      params: {
        skip: 0,
        limit: 10,
        search: '张三'
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error('获取成员列表失败:', error.response.data);
  }
};

// 创建项目
const createProject = async (projectData) => {
  try {
    const response = await axios.post('/api/v1/projects', projectData);
    console.log('项目创建成功:', response.data);
  } catch (error) {
    console.error('项目创建失败:', error.response.data);
  }
};

// 上传文件
const uploadFile = async (file, projectId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('project_id', projectId);
  
  try {
    const response = await axios.post('/api/v1/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log('文件上传成功:', response.data);
  } catch (error) {
    console.error('文件上传失败:', error.response.data);
  }
};
```

### Python/Requests 示例

```python
import requests

# 获取项目列表
def get_projects():
    response = requests.get('http://localhost:8000/api/v1/projects')
    if response.status_code == 200:
        return response.json()
    else:
        print(f'请求失败: {response.status_code}')
        return None

# 创建成员
def create_member(member_data):
    response = requests.post(
        'http://localhost:8000/api/v1/members',
        json=member_data
    )
    if response.status_code == 201:
        return response.json()
    else:
        print(f'创建失败: {response.json()}')
        return None
```

## 注意事项

1. **文件上传限制**: 单个文件最大50MB，批量上传最多10个文件
2. **支持的文件格式**:
   - 文档: PDF, DOC, DOCX, TXT, MD, RTF
   - 图片: JPG, JPEG, PNG, GIF, BMP, WEBP
   - 演示: PPT, PPTX, ODP
   - 视频: MP4, AVI, MOV, WMV, FLV, WEBM
3. **分页**: 默认每页返回100条记录，最大1000条
4. **搜索**: 支持模糊搜索，大小写不敏感
5. **日期格式**: 使用ISO 8601格式 (YYYY-MM-DDTHH:MM:SSZ)

## 更新日志

### v1.0.0 (2024-01-01)

- 初始版本发布
- 实现成员、项目、分享会、设备、值日、文件管理功能
- 提供完整的CRUD操作
- 支持文件上传和下载
- 添加数据统计接口
  