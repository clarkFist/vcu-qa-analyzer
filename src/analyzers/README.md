# Project Analyzers Module

项目分析模块 - 自动分析项目结构、代码质量和依赖关系，生成规范的 HTML 报告。

## 快速开始

### 基本用法

```bash
# 分析当前项目
python analyze_project.py

# 分析指定项目
python analyze_project.py /path/to/project

# 指定输出文件名
python analyze_project.py -o my_analysis_report

# 只生成 Markdown
python analyze_project.py -f markdown

# 只生成 HTML
python analyze_project.py -f html
```

### Python API

```python
from pathlib import Path
from src.analyzers import ReportGenerator

# 生成完整报告
generator = ReportGenerator(Path('.'))
output_files = generator.generate_report(
    output_path=Path('report'),
    format='both'
)

print(f"报告已生成: {output_files}")
```

## 分析器说明

### 1. ProjectAnalyzer - 项目结构分析

分析项目的文件组织、代码统计和目录结构。

**分析内容**:
- 文件总数和目录结构
- 代码行数统计（总行数、代码行、注释行、空行）
- 文件类型分布
- Git 仓库信息
- 项目大小

**使用示例**:
```python
from src.analyzers import ProjectAnalyzer

analyzer = ProjectAnalyzer(Path('/path/to/project'))
result = analyzer.analyze()

print(f"总文件数: {result.data['file_structure']['total_files']}")
print(f"代码行数: {result.data['code_statistics']['code_lines']}")
```

### 2. CodeQualityAnalyzer - 代码质量分析

评估代码质量，包括复杂度、风格和最佳实践。

**分析内容**:
- 圈复杂度计算
- 函数长度检查
- 代码风格问题（行长度、缺失文档字符串）
- 最佳实践检查（测试、README、依赖管理等）

**使用示例**:
```python
from src.analyzers import CodeQualityAnalyzer

analyzer = CodeQualityAnalyzer(Path('/path/to/project'))
result = analyzer.analyze()

complexity = result.data['complexity_analysis']
print(f"平均复杂度: {complexity['average_complexity']}")
print(f"最大复杂度: {complexity['max_complexity']}")
```

### 3. DependencyAnalyzer - 依赖关系分析

分析项目依赖和版本管理。

**分析内容**:
- Python 依赖（requirements.txt, pyproject.toml）
- Node.js 依赖（package.json）
- 版本固定情况分析
- 依赖树生成

**使用示例**:
```python
from src.analyzers import DependencyAnalyzer

analyzer = DependencyAnalyzer(Path('/path/to/project'))
result = analyzer.analyze()

python_deps = result.data['python_dependencies']
if python_deps['found']:
    print(f"Python 包数量: {python_deps['total_count']}")
```

### 4. MetricsCollector - 指标收集器

汇总所有分析结果并计算综合评分。

**评分系统**:
- **总分**: 0-100 分
- **结构评分** (30分): Git 仓库、代码行数、文件多样性
- **质量评分** (40分): 函数长度、代码风格、复杂度
- **实践评分** (30分): 测试、文档、依赖管理

**评级标准**:
- A: 90-100 分
- B: 80-89 分
- C: 70-79 分
- D: 60-69 分
- F: 0-59 分

**使用示例**:
```python
from src.analyzers import MetricsCollector

collector = MetricsCollector(Path('/path/to/project'))
result = collector.analyze()

score = result.data['overall_score']
print(f"综合评分: {score['total']}/100 ({score['grade']})")
```

### 5. ReportGenerator - 报告生成器

将分析结果生成为 Markdown 和 HTML 格式的报告。

**报告内容**:
1. 执行摘要（评分、关键指标、亮点、关注点）
2. 项目结构（文件统计、目录树）
3. 代码质量（复杂度、风格、最佳实践）
4. 依赖分析（Python/Node.js 依赖、版本管理）
5. 诊断信息（错误和警告）

**使用示例**:
```python
from src.analyzers import ReportGenerator

generator = ReportGenerator(Path('/path/to/project'))
output_files = generator.generate_report(
    output_path=Path('analysis_report'),
    format='both'  # 'markdown', 'html', 'both'
)
```

## 扩展分析器

### 创建自定义分析器

1. 继承 `BaseAnalyzer` 类：

```python
from src.analyzers.base import BaseAnalyzer, AnalysisResult
from pathlib import Path

class MyCustomAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisResult:
        # 执行自定义分析
        self.result.data['my_metric'] = self._calculate_my_metric()

        # 添加警告或错误
        if some_condition:
            self.result.add_warning("发现潜在问题")

        return self.result

    def _calculate_my_metric(self):
        # 自定义计算逻辑
        return {"value": 42}
```

2. 在 `MetricsCollector` 中注册：

```python
from .my_custom_analyzer import MyCustomAnalyzer

class MetricsCollector(BaseAnalyzer):
    def analyze(self) -> AnalysisResult:
        # ... 现有代码 ...

        # 添加自定义分析器
        custom_result = MyCustomAnalyzer(self.project_path).analyze()
        self.result.data['custom'] = custom_result.data

        return self.result
```

3. 更新报告模板以显示新指标。

## 配置选项

### 排除目录

默认排除以下目录：
- `__pycache__`, `.git`, `.venv`, `venv`
- `node_modules`, `.pytest_cache`, `.mypy_cache`
- `dist`, `build`, `*.egg-info`

可以在 `BaseAnalyzer._scan_files()` 中自定义排除列表。

### 代码扩展名

默认分析以下代码文件：
- Python: `.py`
- JavaScript/TypeScript: `.js`, `.ts`, `.jsx`, `.tsx`
- C/C++: `.c`, `.cpp`, `.h`
- Java: `.java`

可以在 `ProjectAnalyzer._collect_code_statistics()` 中修改。

## 输出示例

### 命令行输出

```
📊 正在分析项目: my-project
📁 项目路径: /Users/username/projects/my-project

🔍 收集项目信息...

✅ 分析完成！

生成的报告:
  - MARKDOWN: /Users/username/projects/my-project/project_analysis_20251211_134500.md
  - HTML: /Users/username/projects/my-project/project_analysis_20251211_134500.html

💡 提示: 使用浏览器打开 HTML 文件查看完整报告
```

### 报告示例

生成的 HTML 报告包含：
- 交互式目录导航
- 可视化图表（文件类型分布、评分雷达图）
- 语法高亮的代码示例
- 响应式设计，支持移动端查看

## 故障排除

### 常见问题

**Q: 分析失败，提示 "项目路径不存在"**
A: 确保提供的路径是有效的目录路径，使用绝对路径或相对于当前工作目录的路径。

**Q: 无法解析 pyproject.toml**
A: 需要安装 `tomli` 库：`pip install tomli`

**Q: Git 信息无法获取**
A: 确保项目是 Git 仓库，且 `git` 命令在 PATH 中可用。

**Q: 生成的 HTML 报告样式异常**
A: 确保 `src/core/converter.py` 和主题文件正常工作，检查是否有文件权限问题。

### 调试模式

使用 `-v` 参数启用详细输出：

```bash
python analyze_project.py -v
```

这将显示完整的错误堆栈跟踪，帮助诊断问题。

## 性能优化

- 大型项目（>10000 文件）可能需要较长分析时间
- 使用排除目录功能跳过不必要的文件
- 限制分析的文件数量（在代码中调整 `[:20]` 等切片）
- 考虑使用多进程并行分析（未来改进）

## 贡献指南

欢迎贡献新的分析器或改进现有功能！

1. Fork 项目
2. 创建特性分支
3. 实现新分析器（继承 `BaseAnalyzer`）
4. 添加测试用例
5. 提交 Pull Request

## 许可证

与主项目保持一致。

---

**最后更新**: 2025-12-11
**版本**: 1.0.0
