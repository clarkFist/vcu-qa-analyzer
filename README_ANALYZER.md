# 项目分析器 - 快速指南

一个强大的项目分析工具，可以分析任何项目的结构、代码质量和依赖关系，并生成专业的 HTML 报告。

## 🚀 快速开始

### 方式 1: 使用快速脚本（推荐）

```bash
# 分析当前项目
./quick_analyze.sh

# 分析其他项目
./quick_analyze.sh ~/projects/my-app

# 生成 Markdown 报告
./quick_analyze.sh ~/projects/my-app markdown

# 查看帮助
./quick_analyze.sh --help

# 列出常见项目位置
./quick_analyze.sh --list
```

### 方式 2: 使用 Python 命令

```bash
# 分析当前项目
python analyze_project.py

# 分析指定项目
python analyze_project.py /path/to/project

# 自定义输出
python analyze_project.py /path/to/project -o my_report -f html

# 详细模式
python analyze_project.py /path/to/project -v
```

### 方式 3: 使用 Python API

```python
from pathlib import Path
from src.analyzers import ReportGenerator

# 生成报告
generator = ReportGenerator(Path('/path/to/project'))
output_files = generator.generate_report(
    output_path=Path('report'),
    format='both'  # 'markdown', 'html', 'both'
)

print(f"报告已生成: {output_files}")
```

## 📊 分析内容

### 1. 项目结构分析
- ✅ 文件和目录统计
- ✅ 代码行数统计（总行数、代码行、注释行、空行）
- ✅ 文件类型分布
- ✅ 目录树可视化
- ✅ Git 仓库信息
- ✅ 项目大小计算

### 2. 代码质量分析
- ✅ 圈复杂度计算
- ✅ 函数长度检查
- ✅ 代码风格检查
- ✅ 最佳实践验证（测试、文档、依赖管理等）

### 3. 依赖关系分析
- ✅ Python 依赖（requirements.txt, pyproject.toml）
- ✅ Node.js 依赖（package.json）
- ✅ 版本管理分析
- ✅ 依赖树生成

### 4. 综合评分
- ✅ 0-100 分评分系统
- ✅ A-F 等级评定
- ✅ 详细评分细分
- ✅ 改进建议

## 📁 支持的项目类型

- ✅ Python 项目
- ✅ JavaScript/TypeScript 项目
- ✅ Node.js 项目
- ✅ 混合语言项目
- ✅ 文档项目

## 🎯 常见使用场景

### 场景 1: 分析单个项目

```bash
# 使用快速脚本
./quick_analyze.sh ~/projects/my-web-app

# 或使用 Python 命令
python analyze_project.py ~/projects/my-web-app -o webapp_analysis
```

### 场景 2: 批量分析多个项目

```bash
# 创建批量分析脚本
cat > batch_analyze.sh << 'EOF'
#!/bin/bash
for project in ~/projects/*; do
    if [ -d "$project" ]; then
        echo "分析: $(basename $project)"
        ./quick_analyze.sh "$project" html "$(basename $project)_analysis"
    fi
done
EOF

chmod +x batch_analyze.sh
./batch_analyze.sh
```

### 场景 3: 定期生成报告

```bash
# 添加到 crontab（每周一早上 9 点）
0 9 * * 1 cd /path/to/error_report && ./quick_analyze.sh ~/projects/my-app html weekly_report
```

### 场景 4: 集成到 Git Hook

```bash
# .git/hooks/pre-push
#!/bin/bash
python /path/to/error_report/analyze_project.py . -o .reports/pre_push -f markdown

SCORE=$(grep "综合评分" .reports/pre_push.md | grep -oE '[0-9]+' | head -1)

if [ "$SCORE" -lt 60 ]; then
    echo "❌ 代码质量评分过低 ($SCORE/100)"
    exit 1
fi

echo "✅ 代码质量检查通过 ($SCORE/100)"
```

## 📖 详细文档

- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - 如何将分析器应用到其他项目
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - 完整的使用示例和高级用例
- **[src/analyzers/README.md](src/analyzers/README.md)** - 模块详细文档
- **[CLAUDE.md](CLAUDE.md)** - 项目架构和设计文档

## 🔧 安装依赖

```bash
# 安装基础依赖
pip install -r requirements.txt

# 或手动安装
pip install markdown Pygments

# 如果需要解析 pyproject.toml
pip install tomli  # Python < 3.11
```

## 💡 提示和技巧

### 1. 自定义输出目录

```bash
# 设置环境变量
export ANALYZER_OUTPUT_DIR=~/reports

# 所有报告将保存到 ~/reports
./quick_analyze.sh ~/projects/my-app
```

### 2. 排除特定目录

编辑 `src/analyzers/base.py`：

```python
exclude_dirs = [
    '__pycache__', '.git', '.venv', 'venv',
    'node_modules', '.pytest_cache', '.mypy_cache',
    'dist', 'build', '*.egg-info',
    'your_custom_dir',  # 添加自定义排除
]
```

### 3. 修改评分权重

编辑 `src/analyzers/metrics_collector.py`：

```python
# 在 _calculate_overall_score 方法中
structure_score = 30  # 结构评分权重
quality_score = 40    # 质量评分权重
practices_score = 30  # 实践评分权重
```

### 4. 添加自定义分析器

参考 `USAGE_EXAMPLES.md` 中的"自定义分析器"章节。

## 🐛 故障排除

### 问题 1: 提示 "项目路径不存在"

**解决方案**: 确保提供的是有效的目录路径

```bash
# 检查路径是否存在
ls -la /path/to/project

# 使用绝对路径
./quick_analyze.sh /absolute/path/to/project
```

### 问题 2: 缺少依赖

**解决方案**: 安装所需的 Python 包

```bash
pip install -r requirements.txt
```

### 问题 3: Git 信息无法获取

**解决方案**: 确保项目是 Git 仓库

```bash
cd /path/to/project
git status  # 检查是否是 Git 仓库
```

### 问题 4: 分析速度慢

**解决方案**:
1. 增加排除目录
2. 限制分析文件数量
3. 使用 SSD 存储

## 📊 报告示例

生成的 HTML 报告包含：

1. **执行摘要**
   - 综合评分和等级
   - 评分细分
   - 关键指标
   - 亮点和关注点

2. **项目结构**
   - 项目元数据
   - 文件类型分布
   - 代码统计
   - 目录树

3. **代码质量**
   - Python 代码分析
   - 复杂度分析
   - 代码风格
   - 最佳实践

4. **依赖分析**
   - Python/Node.js 依赖
   - 版本管理
   - 依赖树

5. **诊断信息**
   - 错误和警告
   - 改进建议

## 🤝 贡献

欢迎贡献新功能或改进！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

与主项目保持一致。

---

## 快速参考

```bash
# 基本命令
./quick_analyze.sh                          # 分析当前项目
./quick_analyze.sh /path/to/project         # 分析指定项目
./quick_analyze.sh --help                   # 查看帮助
./quick_analyze.sh --list                   # 列出常见项目

# Python 命令
python analyze_project.py                   # 分析当前项目
python analyze_project.py /path/to/project  # 分析指定项目
python analyze_project.py -o report -f html # 自定义输出
python analyze_project.py -v                # 详细模式

# 输出格式
-f markdown    # 只生成 Markdown
-f html        # 只生成 HTML
-f both        # 生成两种格式
```

---

**最后更新**: 2025-12-11
**版本**: 1.0.0
**维护者**: VCU QA Team
