"""
种子数据脚本 - 生成大量 Markdown 文章
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from tortoise import Tortoise
from passlib.hash import bcrypt
from models import User, Article

# ===== 丰富的 Markdown 文章内容 =====

SAMPLE_ARTICLES = [
    {
        "title": "Markdown 语法完全指南",
        "topic": "教程",
        "content": """# Markdown 语法完全指南

## 什么是 Markdown？

Markdown 是一种轻量级标记语言，由 **John Gruber** 于 2004 年创建。它允许人们使用易读易写的纯文本格式编写文档，然后转换成有效的 HTML。

## 基本语法

### 标题

使用 `#` 号可以创建标题：

```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
```

### 强调

- *斜体* 使用单个星号
- **粗体** 使用两个星号
- ***粗斜体*** 使用三个星号
- ~~删除线~~ 使用两个波浪线

### 列表

#### 无序列表

- 苹果
- 香蕉
- 橘子
  - 脐橙
  - 蜜橘

#### 有序列表

1. 第一步
2. 第二步
3. 第三步

### 链接与图片

[访问 GitHub](https://github.com)

![Markdown Logo](https://markdown-here.com/img/icon256.png)

### 代码

行内代码：使用 `console.log('hello')`

代码块：

```javascript
function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet('World'));
```

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(list(fibonacci(10)))
```

### 引用

> 这是引用块
>
> 可以包含多行内容
>
> > 还可以嵌套引用

### 表格

| 名称 | 价格 | 数量 |
|------|------|------|
| 苹果 | ¥5.0 | 100 |
| 香蕉 | ¥3.5 | 200 |
| 橘子 | ¥4.0 | 150 |

### 任务列表

- [x] 学习 Markdown 基础
- [x] 练习常用语法
- [ ] 掌握高级技巧
- [ ] 应用到实际项目

---

*Markdown 让写作更专注，让内容更清晰。*
""",
    },
    {
        "title": "Python 异步编程入门",
        "topic": "编程",
        "content": """# Python 异步编程入门

## 为什么需要异步？

传统的同步编程中，当程序执行 I/O 操作（如网络请求、文件读写）时，CPU 会**空闲等待**，造成资源浪费。

```python
# 同步方式 - 等待 3 秒
import time

def fetch_data(url):
    time.sleep(1)  # 模拟网络延迟
    return f"Data from {url}"

start = time.time()
results = [fetch_data(f"url-{i}") for i in range(3)]
print(f"耗时: {time.time() - start:.2f}s")
# 输出: 耗时: 3.00s
```

## async/await 语法

Python 3.5+ 引入了 `async` 和 `await` 关键字：

```python
import asyncio

async def fetch_data(url):
    await asyncio.sleep(1)  # 非阻塞等待
    return f"Data from {url}"

async def main():
    tasks = [fetch_data(f"url-{i}") for i in range(3)]
    results = await asyncio.gather(*tasks)
    print(results)

start = time.time()
asyncio.run(main())
print(f"耗时: {time.time() - start:.2f}s")
# 输出: 耗时: 1.00s ✨ 快了三倍！
```

## 核心概念

### 协程 (Coroutine)

协程是异步函数，用 `async def` 定义：

```python
async def my_coroutine():
    return 42

# 调用返回协程对象，不会立即执行
coro = my_coroutine()
# 需要 await 或 asyncio.run() 来执行
result = await coro
```

### 可等待对象 (Awaitable)

三种可等待对象：

1. **协程** - `async def` 函数
2. **任务** - `asyncio.Task`，用于并发调度
3. **Future** - 底层接口

### 事件循环 (Event Loop)

事件循环是异步编程的核心调度器：

```python
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

## 实战：并发下载

```python
import asyncio
import aiohttp

async def download_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        "https://example.com",
        "https://httpbin.org/get",
        "https://jsonplaceholder.typicode.com/posts/1",
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [download_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for url, content in zip(urls, results):
            print(f"{url}: {len(content)} bytes")

asyncio.run(main())
```

## 注意事项

> ⚠️ **重要提示**
>
> - 异步代码中不能直接调用阻塞函数
> - 使用 `asyncio.to_thread()` 处理阻塞操作
> - 注意协程的传播性——调用者也需要是 async 函数

## 总结

| 特性 | 同步 | 异步 |
|------|------|------|
| 性能 | I/O 等待浪费 CPU | 等待时执行其他任务 |
| 复杂度 | 简单直观 | 需要理解事件循环 |
| 适用场景 | CPU 密集型 | I/O 密集型 |

> 异步编程不是银弹，但在合适的场景下能带来巨大的性能提升。
""",
    },
    {
        "title": "Vue.js 3 组合式 API 详解",
        "topic": "前端",
        "content": """# Vue.js 3 组合式 API 详解

## 为什么要有组合式 API？

Vue 2 的选项式 API（Options API）在组件逻辑复杂时会出现**代码分散**的问题：

```javascript
// 选项式 API - 同一逻辑分散在不同选项中
export default {
    data() {
        return { count: 0, doubled: 0 }
    },
    watch: {
        count(val) { this.doubled = val * 2 }
    },
    methods: {
        increment() { this.count++ }
    }
}
```

## setup() 函数

组合式 API 的核心是 `setup()` 函数：

```vue
<script>
import { ref, computed, watch, onMounted } from 'vue'

export default {
    setup() {
        // 响应式状态
        const count = ref(0)

        // 计算属性
        const doubled = computed(() => count.value * 2)

        // 监听器
        watch(count, (newVal, oldVal) => {
            console.log(`count 从 ${oldVal} 变为 ${newVal}`)
        })

        // 生命周期
        onMounted(() => {
            console.log('组件已挂载')
        })

        // 方法
        function increment() {
            count.value++
        }

        return { count, doubled, increment }
    }
}
</script>
```

## 核心 API

### ref() - 基本响应式

```javascript
import { ref } from 'vue'

const name = ref('Vue')
console.log(name.value) // 'Vue'

name.value = 'Vue 3'
console.log(name.value) // 'Vue 3'
```

### reactive() - 对象响应式

```javascript
import { reactive } from 'vue'

const state = reactive({
    user: { name: 'Alice', age: 25 },
    todos: ['学习', '编码', '测试']
})

console.log(state.user.name) // 'Alice'
state.todos.push('部署')
```

### computed() - 计算属性

```javascript
import { ref, computed } from 'vue'

const price = ref(100)
const quantity = ref(2)

const total = computed(() => price.value * quantity.value)
```

### watch() - 监听器

```javascript
import { ref, watch } from 'vue'

const searchQuery = ref('')

// 简单监听
watch(searchQuery, (newVal, oldVal) => {
    console.log(`搜索: ${newVal}`)
})

// 深度监听
watch(
    () => state.user,
    (newVal) => {
        console.log('用户信息已更新', newVal)
    },
    { deep: true }
)
```

## 组合式函数 (Composables)

将逻辑提取到可复用的函数中：

```javascript
// useCounter.js
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
    const count = ref(initialValue)

    const doubled = computed(() => count.value * 2)

    function increment() { count.value++ }
    function decrement() { count.value-- }
    function reset() { count.value = initialValue }

    return { count, doubled, increment, decrement, reset }
}
```

在组件中使用：

```vue
<script>
import { useCounter } from './composables/useCounter'

export default {
    setup() {
        const { count, doubled, increment } = useCounter(10)
        return { count, doubled, increment }
    }
}
</script>
```

## 生命周期对比

| Vue 2 (选项式) | Vue 3 (组合式) |
|----------------|----------------|
| beforeCreate   | setup()        |
| created        | setup()        |
| beforeMount    | onBeforeMount  |
| mounted        | onMounted      |
| beforeUpdate   | onBeforeUpdate |
| updated        | onUpdated      |
| beforeUnmount  | onBeforeUnmount|
| unmounted      | onUnmounted    |

## 最佳实践

1. **按功能组织代码**，而不是按选项类型
2. **提取可复用的组合式函数**
3. **使用 `ref()` 处理基本类型，`reactive()` 处理对象**
4. **避免在 `setup()` 中使用 `this`**

> 💡 **提示**：组合式 API 让逻辑复用变得前所未有的简单！
""",
    },
    {
        "title": "Docker 容器化部署实战",
        "topic": "运维",
        "content": """# Docker 容器化部署实战

## 什么是 Docker？

Docker 是一个**容器化平台**，让开发者可以打包应用及其依赖到一个轻量级、可移植的容器中。

## 核心概念

```
┌─────────────────────────────┐
│         Container           │
│  ┌───────────────────────┐  │
│  │      Application      │  │
│  ├───────────────────────┤  │
│  │    Dependencies       │  │
│  ├───────────────────────┤  │
│  │   Operating System    │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

## Dockerfile 编写

```dockerfile
# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## 常用命令

```bash
# 构建镜像
docker build -t myapp:latest .

# 运行容器
docker run -d -p 8000:8000 --name myapp myapp:latest

# 查看容器
docker ps
docker ps -a

# 查看日志
docker logs -f myapp

# 进入容器
docker exec -it myapp bash

# 停止/删除
docker stop myapp
docker rm myapp

# 使用 compose
docker-compose up -d
docker-compose down
```

## 多阶段构建

```dockerfile
# 构建阶段
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 运行阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 最佳实践

### ✅ 应该做的

- 使用 `.dockerignore` 排除不必要的文件
- 尽量使用官方镜像
- 合并 RUN 命令减少层数
- 使用特定版本标签而非 `latest`

### ❌ 避免的

- 不要在容器中存储数据（使用 volumes）
- 不要以 root 用户运行
- 不要硬编码敏感信息

## 总结

> Docker 让"在我机器上能跑"成为历史。
>
> 一次构建，到处运行。 🚀

| 特性 | 虚拟机 | Docker |
|------|--------|--------|
| 启动时间 | 分钟级 | 秒级 |
| 磁盘占用 | GB 级 | MB 级 |
| 性能 | 有损耗 | 接近原生 |
| 隔离性 | 强隔离 | 进程级 |
""",
    },
    {
        "title": "Git 工作流与团队协作",
        "topic": "工具",
        "content": """# Git 工作流与团队协作

## Git 基础

Git 是目前最流行的**分布式版本控制系统**，由 Linus Torvalds 于 2005 年创建。

## 基本工作流

```
工作目录 → 暂存区 → 本地仓库 → 远程仓库
   ↑           ↑          ↑           ↑
 修改文件    git add    git commit   git push
```

## 常用命令

### 配置

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --global core.editor vim
```

### 日常操作

```bash
# 克隆仓库
git clone https://github.com/user/repo.git

# 查看状态
git status
git diff

# 暂存与提交
git add .
git commit -m "feat: add new feature"

# 推送与拉取
git push origin main
git pull origin main

# 分支操作
git branch feature-login
git checkout feature-login
git checkout -b feature-login  # 创建并切换

# 合并
git merge feature-login
```

## Git Flow 工作流

```
main ─────●──────────●──────────●────
           \\        / \\        /
develop     ●──●──●───●──●──●───
             \\    /      \\    /
feature      ●──●──●      ●──●
```

### 分支类型

| 分支 | 用途 | 来源 | 合并到 |
|------|------|------|--------|
| `main` | 生产环境 | - | - |
| `develop` | 开发主线 | main | main |
| `feature/*` | 新功能 | develop | develop |
| `release/*` | 发布准备 | develop | main + develop |
| `hotfix/*` | 紧急修复 | main | main + develop |

## 提交信息规范

使用 **Conventional Commits** 规范：

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### 类型说明

- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具

### 示例

```
feat(auth): add JWT authentication

- Implement login endpoint
- Add token validation middleware
- Update user model

Closes #123
```

## 解决冲突

当合并出现冲突时：

```bash
# 冲突标记
<<<<<<< HEAD
console.log('当前分支的代码')
=======
console.log('合并进来的代码')
>>>>>>> feature-branch

# 解决后
console.log('最终代码')
```

## .gitignore 示例

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.env
venv/

# Node
node_modules/
dist/
npm-debug.log*

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

## 最佳实践

1. **频繁提交**，每次提交只做一件事
2. **写有意义的提交信息**
3. **不要直接推送到 main 分支**
4. **定期 rebase 保持历史清晰**
5. **Code Review 后再合并**

> 💡 **记住**：Git 是你的时间机器，大胆实验，随时可以回退！
""",
    },
    {
        "title": "RESTful API 设计最佳实践",
        "topic": "后端",
        "content": """# RESTful API 设计最佳实践

## 什么是 REST？

REST（Representational State Transfer）是一种**架构风格**，用于设计网络应用程序的 API。

## URL 设计

### 资源命名

```text
✅ 好的设计
GET    /api/users          # 获取用户列表
GET    /api/users/123      # 获取单个用户
POST   /api/users          # 创建用户
PUT    /api/users/123      # 更新用户
DELETE /api/users/123      # 删除用户

❌ 不好的设计
GET    /api/getUsers
POST   /api/createUser
GET    /api/user?id=123
POST   /api/updateUser
```

### 复数名词

```text
✅ /api/articles
✅ /api/comments
✅ /api/categories

❌ /api/article
❌ /api/getArticles
```

## HTTP 方法

| 方法 | 用途 | 幂等 | 安全 |
|------|------|------|------|
| GET | 获取资源 | ✅ | ✅ |
| POST | 创建资源 | ❌ | ❌ |
| PUT | 完整更新 | ✅ | ❌ |
| PATCH | 部分更新 | ❌ | ❌ |
| DELETE | 删除资源 | ✅ | ❌ |

## 状态码

### 2xx 成功

```python
200 OK          # GET 请求成功
201 Created     # POST 创建成功
204 No Content  # DELETE 成功
```

### 3xx 重定向

```python
301 Moved Permanently   # 永久重定向
302 Found               # 临时重定向
304 Not Modified        # 缓存未修改
```

### 4xx 客户端错误

```python
400 Bad Request     # 请求参数错误
401 Unauthorized    # 未认证
403 Forbidden       # 无权限
404 Not Found       # 资源不存在
409 Conflict        # 资源冲突
422 Unprocessable   # 验证失败
429 Too Many Requests  # 请求频率限制
```

### 5xx 服务端错误

```python
500 Internal Server Error   # 服务器内部错误
502 Bad Gateway             # 网关错误
503 Service Unavailable     # 服务不可用
```

## 请求与响应

### 统一响应格式

```json
{
    "success": true,
    "data": {
        "id": "123",
        "title": "Article Title",
        "content": "..."
    },
    "message": "操作成功"
}
```

### 错误响应

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "标题不能为空",
        "details": {
            "field": "title",
            "rule": "required"
        }
    }
}
```

### 分页

```json
GET /api/articles?page=1&page_size=20

{
    "data": [...],
    "pagination": {
        "page": 1,
        "page_size": 20,
        "total": 100,
        "total_pages": 5
    }
}
```

## 认证与授权

### JWT 认证

```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "***"
}

Response:
{
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 3600
}
```

### 使用 Token

```http
GET /api/articles
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## 版本控制

```text
# 方式一：URL 路径
/api/v1/users
/api/v2/users

# 方式二：请求头
Accept: application/vnd.api+json;version=1
```

## 过滤、排序、搜索

```text
# 过滤
GET /api/articles?category=tech&status=published

# 排序
GET /api/articles?sort=-created_at
GET /api/articles?sort=title,-created_at

# 搜索
GET /api/articles?search=keyword

# 字段选择
GET /api/articles?fields=id,title,created_at
```

## 速率限制

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1620000000
```

## 总结

> 好的 API 设计应该像好的代码一样：**简单、一致、可预测**。

### 核心原则

1. ✅ 使用名词而非动词
2. ✅ 使用复数形式
3. ✅ 正确的 HTTP 方法和状态码
4. ✅ 统一的错误格式
5. ✅ 支持分页和过滤
6. ✅ 版本控制
7. ✅ 安全的认证机制
""",
    },
    {
        "title": "Linux 命令行效率提升技巧",
        "topic": "运维",
        "content": """# Linux 命令行效率提升技巧

## 终端快捷键

### 光标移动

```bash
Ctrl + A    # 移动到行首
Ctrl + E    # 移动到行尾
Ctrl + ←    # 向左跳一个词
Ctrl + →    # 向右跳一个词
Alt + B     # 向后跳一个词
Alt + F     # 向前跳一个词
```

### 编辑

```bash
Ctrl + U    # 删除到行首
Ctrl + K    # 删除到行尾
Ctrl + W    # 删除前一个词
Alt + D     # 删除后一个词
Ctrl + Y    # 粘贴删除的内容
```

### 历史命令

```bash
Ctrl + R    # 搜索历史命令
Ctrl + P    # 上一条命令
Ctrl + N    # 下一条命令
!!          # 执行上一条命令
!$          # 上一条命令的最后一个参数
!*          # 上一条命令的所有参数
```

## 文件操作

### 查找文件

```bash
# 按名称查找
find /home -name "*.py"

# 按类型查找
find . -type f -name "*.log"

# 按大小查找
find . -size +100M

# 按时间查找
find . -mtime -7  # 7天内修改

# 执行操作
find . -name "*.tmp" -delete
```

### 内容搜索

```bash
# 递归搜索
grep -r "function" src/

# 显示行号
grep -n "error" app.log

# 忽略大小写
grep -i "warning" *.log

# 显示上下文
grep -C 3 "exception" trace.log

# 只显示文件名
grep -l "TODO" src/**/*.py
```

## 文本处理

### sed - 流编辑器

```bash
# 替换文本
sed 's/old/new/g' file.txt

# 原地替换
sed -i 's/foo/bar/g' config.ini

# 删除行
sed '/^#/d' config.ini  # 删除注释行

# 打印特定行
sed -n '10,20p' file.txt
```

### awk - 文本分析

```bash
# 打印特定列
awk '{print $1, $3}' data.txt

# 带条件
awk '$3 > 100 {print $1, $3}' data.txt

# 自定义分隔符
awk -F: '{print $1}' /etc/passwd

# 统计
awk '{sum += $1} END {print sum}' numbers.txt
```

## 进程管理

```bash
# 查看进程
ps aux
ps aux | grep python

# 树形结构
pstree

# 实时监控
top
htop

# 杀死进程
kill -9 PID
killall python

# 后台运行
nohup python script.py &
disown
```

## 网络工具

```bash
# 网络连接
netstat -tuln
ss -tuln

# HTTP 请求
curl -X GET https://api.example.com
curl -X POST -d '{"key":"value"}' -H "Content-Type: application/json" https://api.example.com

# 下载文件
wget https://example.com/file.zip

# DNS 查询
nslookup google.com
dig google.com

# 端口测试
telnet host 80
nc -zv host 80
```

## 磁盘与内存

```bash
# 磁盘使用
df -h
du -sh *

# 最大的文件
du -sh * | sort -rh | head -10

# 内存使用
free -h
vmstat 1

# I/O 监控
iostat -x 1
iotop
```

## 实用技巧

### 别名

```bash
# 常用别名
alias ll='ls -alF'
alias ..='cd ..'
alias gs='git status'
alias gc='git commit'
alias gp='git push'

# 保存到 ~/.bashrc
echo "alias ll='ls -alF'" >> ~/.bashrc
```

### 一行命令

```bash
# 统计代码行数
find . -name "*.py" -exec cat {} \; | wc -l

# 批量重命名
for f in *.txt; do mv "$f" "${f%.txt}.md"; done

# 监控日志
tail -f app.log | grep ERROR

# 压缩备份
tar -czf backup.tar.gz --exclude=node_modules .
```

## 总结

> 掌握命令行，让你的效率提升 10 倍！🚀

| 技能 | 节省时间 | 学习难度 |
|------|----------|----------|
| 快捷键 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| find/grep | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| sed/awk | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 别名 | ⭐⭐⭐ | ⭐ |
""",
    },
    {
        "title": "JavaScript 异步编程进化史",
        "topic": "前端",
        "content": """# JavaScript 异步编程进化史

## 回调地狱时代

在 ES6 之前，JavaScript 处理异步只能靠**回调函数**：

```javascript
// 回调地狱 😱
getUser(1, (user) => {
    getPosts(user.id, (posts) => {
        getComments(posts[0].id, (comments) => {
            getLikes(comments[0].id, (likes) => {
                console.log('终于拿到数据了！', likes);
            });
        });
    });
});
```

这种代码被称为**"回调地狱"（Callback Hell）**，难以阅读和维护。

## Promise 时代

ES6 引入了 **Promise**，让异步代码有了链式调用的能力：

```javascript
// Promise 链
getUser(1)
    .then(user => getPosts(user.id))
    .then(posts => getComments(posts[0].id))
    .then(comments => getLikes(comments[0].id))
    .then(likes => {
        console.log('数据：', likes);
    })
    .catch(error => {
        console.error('出错了：', error);
    });
```

### 创建 Promise

```javascript
function fetchData(url) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (url) {
                resolve(`数据来自 ${url}`);
            } else {
                reject(new Error('URL 不能为空'));
            }
        }, 1000);
    });
}

// 使用
fetchData('/api/data')
    .then(data => console.log(data))
    .catch(err => console.error(err));
```

### Promise 静态方法

```javascript
// 并行执行
Promise.all([
    fetch('/api/users'),
    fetch('/api/posts'),
    fetch('/api/comments')
]).then(([users, posts, comments]) => {
    console.log('全部完成！');
});

// 竞速
Promise.race([
    fetch('/api/data'),
    fetch('/api/backup')
]).then(data => {
    console.log('谁先返回用谁：', data);
});

// 全部完成（不管成功失败）
Promise.allSettled([
    fetch('/api/data'),
    fetch('/api/error')
]).then(results => {
    results.forEach(r => {
        console.log(r.status); // 'fulfilled' 或 'rejected'
    });
});
```

## async/await 时代

ES2017 引入了 **async/await**，让异步代码看起来像同步代码：

```javascript
// 优雅的异步代码 ✨
async function fetchAllData() {
    try {
        const user = await getUser(1);
        const posts = await getPosts(user.id);
        const comments = await getComments(posts[0].id);
        const likes = await getLikes(comments[0].id);
        
        return { user, posts, comments, likes };
    } catch (error) {
        console.error('获取数据失败：', error);
        throw error;
    }
}

// 使用
fetchAllData().then(data => {
    console.log('所有数据：', data);
});
```

### 并行与串行

```javascript
// 串行执行（慢）
async function serial() {
    const a = await fetchA();
    const b = await fetchB();
    const c = await fetchC();
    return [a, b, c]; // 耗时 3 秒
}

// 并行执行（快！）
async function parallel() {
    const [a, b, c] = await Promise.all([
        fetchA(),
        fetchB(),
        fetchC()
    ]);
    return [a, b, c]; // 耗时 1 秒
}
```

## 实际应用

### 带超时的请求

```javascript
async function fetchWithTimeout(url, timeout = 5000) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(url, {
            signal: controller.signal
        });
        return await response.json();
    } finally {
        clearTimeout(timer);
    }
}
```

### 重试机制

```javascript
async function fetchWithRetry(url, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            if (i === retries - 1) throw error;
            console.log(`第 ${i + 1} 次重试...`);
            await new Promise(r => setTimeout(r, 1000 * (i + 1)));
        }
    }
}
```

## 性能对比

| 方式 | 可读性 | 错误处理 | 并行能力 |
|------|--------|----------|----------|
| 回调 | ⭐ | ⭐ | ⭐⭐⭐ |
| Promise | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| async/await | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 总结

> JavaScript 异步编程的进化：
>
> **回调 → Promise → async/await**
>
> 每一次进化都让代码更优雅、更易维护。🎯
""",
    },
    {
        "title": "数据库索引原理与优化",
        "topic": "后端",
        "content": """# 数据库索引原理与优化

## 为什么需要索引？

想象一本没有目录的书——要找到某个知识点，你得**从头翻到尾**。这就是**全表扫描**。

索引就是数据库的**目录**，让你能快速定位数据。

## 索引的数据结构

### B+ 树

MySQL 的 InnoDB 引擎使用 **B+ 树** 作为索引结构：

```
             [50]
            /    \\
       [20, 30]   [70, 90]
      /    |   \   |   \\
    [1,5] [21,25] [31,35] [51,55] [71,75] [91,95]
```

**特点：**
- 所有数据都在叶子节点
- 叶子节点形成有序链表
- 非叶子节点只存索引
- 树的高度通常为 3-4 层

### 哈希索引

```sql
-- 哈希索引适合等值查询
SELECT * FROM users WHERE id = 100;  -- O(1)

-- 不适合范围查询
SELECT * FROM users WHERE id > 100;  -- 需要全扫描
```

## 索引类型

### 主键索引

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,  -- 自动创建主键索引
    name VARCHAR(50),
    email VARCHAR(100)
);
```

### 唯一索引

```sql
CREATE UNIQUE INDEX idx_email ON users(email);
-- 或
ALTER TABLE users ADD UNIQUE INDEX idx_email(email);
```

### 普通索引

```sql
CREATE INDEX idx_name ON users(name);
```

### 复合索引

```sql
-- 最左前缀原则
CREATE INDEX idx_name_age ON users(name, age);

-- 能用到索引的查询
WHERE name = 'Alice'           -- ✅
WHERE name = 'Alice' AND age = 25  -- ✅
WHERE name LIKE 'Ali%'         -- ✅

-- 用不到索引的查询
WHERE age = 25                 -- ❌ 跳过了 name
WHERE name LIKE '%lice'        -- ❌ 前缀模糊
```

## 执行计划分析

```sql
-- 查看查询是否用到索引
EXPLAIN SELECT * FROM users WHERE name = 'Alice';

-- 输出关键字段
-- type: ALL（全表扫描）, ref（索引查找）, const（主键查找）
-- key: 实际使用的索引
-- rows: 扫描的行数
-- Extra: Using index（覆盖索引）, Using filesort（文件排序）
```

## 索引优化策略

### 1. 选择合适的列

```sql
-- ✅ 适合索引
-- 高选择性的列（唯一值多）
-- WHERE 条件中的列
-- JOIN 的关联列
-- ORDER BY 的列

-- ❌ 不适合索引
-- 低选择性的列（如性别）
-- 频繁更新的列
-- 大文本字段
```

### 2. 覆盖索引

```sql
-- 索引包含所有需要的字段，无需回表
CREATE INDEX idx_cover ON users(name, email, age);

-- 以下查询只需从索引读取，无需回表
SELECT name, email FROM users WHERE name = 'Alice';  -- ✅ 覆盖索引
SELECT name FROM users WHERE age > 18;               -- ❌ 不是覆盖索引
```

### 3. 避免索引失效

```sql
-- ❌ 索引列上使用函数
WHERE YEAR(created_at) = 2024

-- ✅ 改为范围查询
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'

-- ❌ 隐式类型转换
WHERE phone = 13800138000  -- phone 是字符串

-- ✅ 使用字符串
WHERE phone = '13800138000'
```

## 索引维护

```sql
-- 查看索引使用情况
SHOW INDEX FROM users;

-- 分析查询
EXPLAIN ANALYZE SELECT * FROM users WHERE name = 'Alice';

-- 重建索引
ALTER TABLE users DROP INDEX idx_name;
ALTER TABLE users ADD INDEX idx_name(name);
```

## 实战案例

### 慢查询优化

```sql
-- 原始查询（全表扫描，10 秒）
SELECT * FROM orders
WHERE status = 'pending'
  AND created_at > '2024-01-01'
ORDER BY amount DESC;

-- 添加复合索引后（0.01 秒）
CREATE INDEX idx_status_created_amount
ON orders(status, created_at, amount DESC);
```

### 分页优化

```sql
-- 传统分页（越往后越慢）
SELECT * FROM articles
ORDER BY id
LIMIT 100000, 20;

-- 优化：基于游标的分页
SELECT * FROM articles
WHERE id > 100000
ORDER BY id
LIMIT 20;
```

## 总结

| 索引类型 | 适用场景 | 注意事项 |
|----------|----------|----------|
| 主键索引 | 唯一标识 | 自增或 UUID |
| 唯一索引 | 防止重复 | 影响写入性能 |
| 复合索引 | 多条件查询 | 最左前缀原则 |
| 全文索引 | 文本搜索 | 占用空间大 |

> 💡 **记住**：索引不是越多越好，每个索引都会影响写入性能。
>
> **权衡的艺术**：查询速度 vs 写入速度 vs 存储空间。
""",
    },
]

async def seed():
    db_path = os.path.join(os.path.dirname(__file__), "db.sqlite3")
    await Tortoise.init(
        db_url=f"sqlite://{db_path}",
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()

    # 获取管理员用户
    admin = await User.get_or_none(username="admin")
    if not admin:
        print("[!] 管理员用户不存在，请先启动后端服务")
        return

    # 检查是否已有文章
    existing = await Article.all().count()
    if existing > 0:
        print(f"[!] 数据库中已有 {existing} 篇文章，跳过种子数据")
        print("    如需重新导入，请先清空数据库")
        return

    print(f"正在导入 {len(SAMPLE_ARTICLES)} 篇文章...")
    for i, item in enumerate(SAMPLE_ARTICLES, 1):
        await Article.create(
            author=admin,
            title=item["title"],
            content=item["content"],
            topic=item["topic"],
            is_published=True,
        )
        print(f"  [{i}/{len(SAMPLE_ARTICLES)}] {item['title']}")

    print(f"\n✅ 成功导入 {len(SAMPLE_ARTICLES)} 篇文章！")
    print("   登录账号: admin / admin123")
    print("   前端地址: http://localhost:8080")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(seed())

