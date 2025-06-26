# vcpkg 依赖库查询工具

一个用于查询 vcpkg 依赖库版本信息和最新 commit SHA 的 Python 工具。

## 🚀 功能特性

- **交互式查询**: 用户友好的命令行界面
- **版本管理**: 自动获取并显示所有可用版本
- **智能推荐**: 当输入错误的库名时，提供5个最相似的推荐
- **GitHub集成**: 直接通过 GitHub API 获取最新信息
- **批量查询**: 支持连续查询多个依赖库
- **GitHub Token支持**: 支持个人访问令牌以提高API限制
- **所有版本及SHA**: 一次性展示所有版本及其 commit SHA

## 📋 系统要求

- Python 3.6 或更高版本
- Windows 操作系统（批处理文件）

## 🔑 GitHub Token 设置（推荐）

为了获得更好的API访问限制，建议设置GitHub个人访问令牌：

### 1. 创建GitHub Token
1. 访问 [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token (classic)"
3. 选择 "public_repo" 权限
4. 生成并复制token

### 2. 使用Token
- 运行脚本时会提示是否使用GitHub Token
- 选择 "y" 并输入你的token
- Token输入时会被隐藏，保护隐私

### API限制对比
- **匿名访问**: 60次/小时
- **使用Token**: 5000次/小时

## 🛠️ 安装步骤

### 1. 克隆或下载项目
```bash
git clone <repository-url>
cd vcpkg
```

### 2. 安装依赖包
双击运行 `install_dependencies.bat` 文件，或在命令行中执行：
```bash
pip install -r requirements.txt
```

## 🎯 使用方法

### 运行脚本
```bash
python vcpkg-get-commit-sha.py
```

### 使用流程

1. **Token设置**: 选择是否使用GitHub Token（推荐）
2. **启动程序**: 运行脚本后，会显示欢迎信息
3. **输入库名**: 输入你想要查询的依赖库名称
4. **查看所有版本及SHA**: 自动展示所有版本及其 commit SHA
5. **选择版本**: 如果有多个版本，选择你需要的版本
6. **查看结果**: 获取依赖库信息、版本和最新Commit SHA
7. **继续查询**: 选择是否继续查询其他依赖库

### 示例输出
```
🚀 vcpkg 依赖库查询工具
==================================================

🔑 GitHub Token 设置
==============================
💡 提示：
1. 访问 https://github.com/settings/tokens 创建个人访问令牌
2. 选择 'public_repo' 权限即可
3. 如果不输入token，将使用匿名访问（限制更严格）

是否使用GitHub Token？(y/n): y
请输入你的GitHub Token: ********
✅ Token已设置
✅ 使用GitHub Token，API限制：5000次/小时

🔍 正在获取所有可用的依赖库列表...
✅ 成功获取 2667 个依赖库

请输入你想要查询的依赖库名称 (输入 'quit' 退出): qtbase

📋 qtbase 的所有版本及其 commit SHA：
版本                 commit SHA
------------------------------------------------------------
6.8.3                1234567890abcdef...
6.8.2                abcdef1234567890...
6.8.1                1122334455667788...
...

📋 qtbase 的所有可用版本：
   1. 6.8.3
   2. 6.8.2
   3. 6.8.1

请选择版本 (1-3) 或直接回车使用最新版本: 1

✅ 选择的版本: 6.8.3
📦 正在查询 qtbase 的最新 commit SHA...

📋 查询结果：
依赖库: qtbase
版本: 6.8.3
最新Commit SHA: 1234567890abcdef...

是否继续查询其他依赖库？(y/n): n
👋 再见！
```

## 🔧 错误处理

### 库名不存在
如果输入的依赖库名称不存在，程序会提供相似名称的推荐：
```
❌ 未找到依赖库 'qtbas'
  也许你想要的是以下这些依赖库：
   1. qtbase
   2. qtbaseline
   3. qtbase64
   4. qtbase32
   5. qtbase16

请重新输入正确的依赖库名称
```

### GitHub API限制
- **匿名访问**: 遇到限制时会提示使用Token
- **Token访问**: 遇到限制时会检查Token权限
- **Token无效**: 会提示检查Token是否正确

### 网络错误
如果网络连接有问题，程序会显示相应的错误信息。

## 📁 文件结构

```
vcpkg/
├── vcpkg-get-commit-sha.py    # 主程序脚本
├── requirements.txt           # Python依赖包列表
├── install_dependencies.bat   # 依赖安装批处理文件
└── README.md                 # 说明文档
```

## 🔍 支持的依赖库

该工具支持查询 vcpkg 仓库中的所有可用依赖库，包括但不限于：
- Qt 相关库 (qtbase, qtconnectivity, qttools 等)
- 系统库 (openssl, boost, eigen 等)
- 图形库 (opencv, sdl2, glfw 等)
- 其他常用库

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具！

## 📄 许可证

本项目采用 MIT 许可证。

## 🔗 相关链接

- [vcpkg GitHub 仓库](https://github.com/microsoft/vcpkg)
- [vcpkg 官方文档](https://vcpkg.io/)
- [Python 官网](https://www.python.org/)
- [GitHub Token 设置](https://github.com/settings/tokens) 