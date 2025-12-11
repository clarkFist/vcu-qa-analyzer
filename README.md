# VCU QA Document Generator & AI Project Analyzer

优雅的 Markdown 转 HTML 报告生成工具 + AI 驱动的项目分析系统，专为 VCU（车辆控制单元）项目质量文档和技术报告设计。

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

## 🎯 核心功能

### 1. Markdown 转 HTML 报告生成

- ✅ 将 Markdown 技术文档转换为专业的 HTML 报告
- ✅ 支持图片自动嵌入（Base64）
- ✅ 支持 Mermaid 图表渲染
- ✅ 多主题支持（默认、极简、专业）
- ✅ 批量处理和交互式界面

### 2. 项目分析与质量报告

- ✅ 自动分析项目结构、代码质量、依赖关系
- ✅ 生成综合评分（0-100 分，A-F 等级）
- ✅ 提供详细的改进建议
- ✅ 支持 Python 和 Node.js 项目

### 3. AI 驱动的智能 Skills

- ✅ **项目问答**: 像与专家对话一样询问项目相关问题
- ✅ **代码洞察**: 深度代码分析和架构模式识别
- ✅ **智能建议**: 基于分析结果提供改进建议

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### Markdown 转 HTML

```bash
# 单文件转换
python md2html.py report.md

# 批量转换
python md2html.py docs/ -r -o output/

# 交互式模式
python md2html.py
```

### 项目分析

```bash
# 分析当前项目
python analyze_project.py

# 分析指定项目
python analyze_project.py /path/to/project

# 使用快速脚本
bash quick_analyze.sh ~/projects/my-app
```

### AI 智能问答

```bash
# 启动交互式问答
python skills/project_qa.py /path/to/project

# 单个问题
python skills/project_qa.py /path/to/project -q "项目结构如何？"

# 代码洞察
python skills/code_insight.py /path/to/project
```

## 📚 文档

- **[CLAUDE.md](CLAUDE.md)** - 项目架构和设计文档
- **[SKILLS_GUIDE.md](SKILLS_GUIDE.md)** - AI Skills 完整使用指南
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - 使用示例和高级用例
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - 迁移和集成指南
- **[README_ANALYZER.md](README_ANALYZER.md)** - 项目分析器快速指南

## 🎨 特色功能

### Markdown 转换

- **多主题支持**: 默认、极简、专业三种主题
- **图片嵌入**: 自动将图片转换为 Base64 嵌入 HTML
- **Mermaid 图表**: 支持流程图、序列图、甘特图等
- **语法高亮**: 使用 Pygments 进行代码高亮
- **响应式设计**: 支持移动端查看

### 项目分析

- **结构分析**: 文件统计、目录树、文件类型分布
- **质量评估**: 圈复杂度、代码风格、最佳实践检查
- **依赖分析**: Python/Node.js 依赖解析和版本管理
- **综合评分**: 0-100 分评分系统，A-F 等级评定

### AI Skills

- **智能问答**: 回答关于项目的各种问题
- **架构识别**: 自动识别 MVC、分层架构、微服务等模式
- **代码异味**: 检测长方法、大类、参数过多等问题
- **函数分析**: 识别递归、生成器、异步函数等特征

## 💡 使用场景

### 场景 1: 技术文档生成

```bash
# 将 Markdown 文档转换为专业 HTML 报告
python md2html.py technical_report.md -t professional --embed-images --mermaid
```

### 场景 2: 项目质量评估

```bash
# 生成项目分析报告
python analyze_project.py ~/projects/my-app -o quality_report
```

### 场景 3: 快速了解新项目

```bash
# 启动 AI 问答
python skills/project_qa.py ~/new-project

# 问一些问题
❓ 项目结构如何？
❓ 代码质量怎么样？
❓ 有什么改进建议？
```

### 场景 4: 代码审查

```bash
# 运行代码洞察
python skills/code_insight.py ~/project-to-review
```

## 🏗️ 项目结构

```
.
├── md2html.py              # Markdown 转 HTML 入口
├── analyze_project.py      # 项目分析入口
├── quick_analyze.sh        # 快速分析脚本
├── src/
│   ├── analyzers/          # 项目分析模块
│   │   ├── base.py
│   │   ├── project_analyzer.py
│   │   ├── code_quality_analyzer.py
│   │   ├── dependency_analyzer.py
│   │   ├── metrics_collector.py
│   │   └── report_generator.py
│   ├── core/               # 核心转换引擎
│   ├── processors/         # 图片和 Mermaid 处理器
│   ├── themes/             # HTML 主题
│   └── utils/              # 工具函数
├── skills/                 # AI Skills 模块
│   ├── project_qa.py       # 项目问答
│   ├── code_insight.py     # 代码洞察
│   └── skill_manager.py    # Skills 管理器
└── legacy/                 # 历史 VCU 报告
```

## 🔧 技术栈

- **Python 3.9+**
- **Markdown**: python-markdown
- **语法高亮**: Pygments
- **代码分析**: AST (Abstract Syntax Tree)
- **图表渲染**: Mermaid.js (客户端)

## 📊 项目统计

- **总文件数**: 50+
- **代码行数**: 5000+
- **Python 文件**: 33
- **Markdown 文档**: 12
- **支持的主题**: 3
- **AI Skills**: 2

## 🤝 贡献

欢迎贡献新功能或改进！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License

## 🙏 致谢

- VCU 项目团队
- Claude AI (Anthropic)
- 所有贡献者

## 📞 联系方式

- **项目主页**: [GitHub Repository]
- **问题反馈**: [GitHub Issues]
- **文档**: 查看项目中的 Markdown 文档

---

**最后更新**: 2025-12-11
**版本**: 1.0.0
**维护者**: VCU QA Team

---

## 🎓 快速参考

### Markdown 转换

```bash
python md2html.py file.md                    # 基本转换
python md2html.py file.md -t minimal         # 使用极简主题
python md2html.py docs/ -r -o output/        # 批量转换
```

### 项目分析

```bash
python analyze_project.py                    # 分析当前项目
python analyze_project.py /path/to/project   # 分析指定项目
bash quick_analyze.sh ~/projects/my-app      # 快速分析
```

### AI Skills

```bash
python skills/project_qa.py /path/to/project              # 交互式问答
python skills/project_qa.py /path/to/project -q "问题"    # 单个问题
python skills/code_insight.py /path/to/project            # 代码洞察
python skills/skill_manager.py /path/to/project           # Skills 管理器
```
