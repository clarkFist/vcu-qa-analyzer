# AI 驱动的 Skills 系统

基于项目分析的智能问答和代码洞察系统。

## 🎯 核心概念

**Skills** 是 AI 驱动的功能模块，可以：
- 分析项目结构和代码
- 回答关于项目的问题
- 提供智能建议和洞察
- 检测代码问题和架构模式

## 📦 可用的 Skills

### 1. 项目问答 (project_qa)

智能问答系统，可以回答关于项目的各种问题。

**功能**:
- 项目结构分析
- 代码质量评估
- 依赖关系查询
- 评分和建议
- 文件列表查询

**使用示例**:

```bash
# 交互式模式
python skills/project_qa.py /path/to/project

# 单个问题
python skills/project_qa.py /path/to/project -q "项目结构如何？"

# JSON 输出
python skills/project_qa.py /path/to/project -q "代码质量怎么样？" --json
```

**支持的问题类型**:

| 问题类型 | 示例问题 |
|---------|---------|
| 结构 | "项目结构如何？"、"有哪些目录？" |
| 质量 | "代码质量怎么样？"、"复杂度如何？" |
| 依赖 | "有哪些依赖？"、"使用了什么包？" |
| 评分 | "项目评分是多少？"、"等级是什么？" |
| 文件 | "有哪些 Python 文件？"、"包含什么文件？" |
| 改进 | "有什么改进建议？"、"如何优化？" |

### 2. 代码洞察 (code_insight)

深度代码分析，提供架构和代码质量洞察。

**功能**:
- 架构模式识别（MVC、分层架构、微服务等）
- 代码异味检测（长方法、大类、参数过多等）
- 导入依赖图构建
- 函数特征分析（递归、生成器、异步等）
- 类层次分析

**使用示例**:

```bash
# 完整分析
python skills/code_insight.py /path/to/project

# 特定类别
python skills/code_insight.py /path/to/project -c architecture_patterns

# JSON 输出
python skills/code_insight.py /path/to/project --json
```

**分析类别**:
- `architecture_patterns` - 架构模式
- `code_smells` - 代码异味
- `import_graph` - 导入依赖图
- `function_analysis` - 函数分析
- `class_hierarchy` - 类层次

## 🚀 快速开始

### 方式 1: 使用 Skill 管理器（推荐）

```bash
# 交互式模式
python skills/skill_manager.py /path/to/project

# 列出所有 Skills
python skills/skill_manager.py /path/to/project --list

# 执行特定 Skill
python skills/skill_manager.py /path/to/project --skill qa --question "项目结构如何？"
python skills/skill_manager.py /path/to/project --skill insight
```

### 方式 2: 直接使用 Skill

```bash
# 项目问答
python skills/project_qa.py ~/projects/my-app

# 代码洞察
python skills/code_insight.py ~/projects/my-app
```

### 方式 3: Python API

```python
from pathlib import Path
from skills.skill_manager import SkillManager

# 初始化管理器
manager = SkillManager(Path('/path/to/project'))

# 使用问答 Skill
result = manager.execute('qa', 'ask', question="项目结构如何？")
print(result['answer'])

# 使用洞察 Skill
insight_skill = manager.get_skill('insight')
print(insight_skill.format_insights())
```

## 💡 使用场景

### 场景 1: 快速了解新项目

```bash
# 启动交互式问答
python skills/project_qa.py ~/projects/new-project

# 问一些问题
❓ 您的问题: 项目结构如何？
❓ 您的问题: 代码质量怎么样？
❓ 您的问题: 有哪些依赖？
❓ 您的问题: 有什么改进建议？
```

### 场景 2: 代码审查

```bash
# 运行代码洞察
python skills/code_insight.py ~/projects/my-app

# 查看检测到的问题
# - 架构模式
# - 代码异味
# - 函数特征
# - 类层次
```

### 场景 3: 批量项目分析

```python
from pathlib import Path
from skills.skill_manager import SkillManager

projects = [
    Path('~/projects/app1'),
    Path('~/projects/app2'),
    Path('~/projects/app3'),
]

for project in projects:
    print(f"\n分析项目: {project.name}")
    print("=" * 60)

    manager = SkillManager(project)

    # 获取评分
    result = manager.execute('qa', 'ask', question="项目评分是多少？")
    print(result['answer'])

    # 获取改进建议
    result = manager.execute('qa', 'ask', question="有什么改进建议？")
    print(result['answer'])
```

### 场景 4: 集成到 CI/CD

```yaml
# .github/workflows/code-analysis.yml
name: Code Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run code insight
        run: |
          python skills/code_insight.py . --json > insights.json

      - name: Check code smells
        run: |
          SMELLS=$(python -c "import json; data=json.load(open('insights.json')); print(len(data['code_smells']))")
          if [ "$SMELLS" -gt 10 ]; then
            echo "Too many code smells detected: $SMELLS"
            exit 1
          fi
```

## 🔧 扩展 Skills

### 创建新的 Skill

```python
# skills/my_skill.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

class MySkill:
    """自定义 Skill"""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self._analyze()

    def _analyze(self):
        """分析逻辑"""
        print("🔍 正在分析...")
        # 您的分析代码
        print("✅ 分析完成\n")

    def my_action(self, param: str):
        """自定义操作"""
        # 您的操作逻辑
        return {"result": "success"}

def main():
    import argparse

    parser = argparse.ArgumentParser(description='My Custom Skill')
    parser.add_argument('project_path', help='项目路径')
    args = parser.parse_args()

    skill = MySkill(Path(args.project_path))
    # 使用 skill

if __name__ == '__main__':
    main()
```

### 注册到管理器

编辑 `skills/skill_manager.py`：

```python
from skills.my_skill import MySkill

class SkillManager:
    def _register_skills(self):
        self.skills = {
            # ... 现有 skills ...
            'my_skill': {
                'name': '我的 Skill',
                'description': 'Skill 描述',
                'class': MySkill,
                'instance': None
            }
        }
```

## 📊 输出格式

### 文本格式

```
📁 项目结构分析：

**基本信息**
- 项目名称: my-project
- 项目类型: Python
- 项目大小: 1.2 MB
- 总文件数: 45

**文件类型分布**
- .py: 30 个文件
- .md: 5 个文件
- .json: 3 个文件
```

### JSON 格式

```json
{
  "question": "项目结构如何？",
  "type": "structure",
  "answer": "...",
  "details": {
    "total_files": 45,
    "file_types": {
      "py": 30,
      "md": 5,
      "json": 3
    },
    "project_size": "1.2 MB"
  }
}
```

## 🎨 高级用法

### 1. 自定义问题分类

编辑 `skills/project_qa.py` 中的 `_classify_question` 方法：

```python
def _classify_question(self, question: str) -> str:
    keywords = {
        'structure': ['结构', '目录', 'structure'],
        'quality': ['质量', '复杂度', 'quality'],
        'my_category': ['自定义', '关键词'],  # 添加新类别
    }
    # ...
```

### 2. 添加新的分析维度

在 `skills/code_insight.py` 中添加新的分析方法：

```python
def _analyze_security(self, python_files: List[Path]) -> Dict[str, Any]:
    """安全性分析"""
    security_issues = []

    for file_path in python_files:
        # 检查安全问题
        # ...

    return {'issues': security_issues}
```

### 3. 集成外部工具

```python
import subprocess

def _run_pylint(self, file_path: Path) -> Dict[str, Any]:
    """运行 pylint"""
    result = subprocess.run(
        ['pylint', str(file_path), '--output-format=json'],
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)
```

## 🐛 故障排除

### 问题 1: 导入错误

**错误**: `ModuleNotFoundError: No module named 'src'`

**解决方案**: 确保从项目根目录运行脚本

```bash
cd /path/to/error_report
python skills/project_qa.py /path/to/target/project
```

### 问题 2: 分析速度慢

**解决方案**: 限制分析的文件数量

编辑 Skill 文件，修改切片：

```python
for file_path in python_files[:10]:  # 只分析前 10 个文件
    # ...
```

### 问题 3: 内存占用高

**解决方案**: 使用生成器而非列表

```python
def _scan_files_generator(self):
    for file_path in self.project_path.rglob("*.py"):
        yield file_path
```

## 📚 相关文档

- [项目分析模块](../src/analyzers/README.md)
- [使用示例](../USAGE_EXAMPLES.md)
- [迁移指南](../MIGRATION_GUIDE.md)

## 🤝 贡献

欢迎贡献新的 Skills！

1. 创建新的 Skill 文件
2. 实现必要的方法
3. 注册到 SkillManager
4. 添加文档和示例
5. 提交 Pull Request

---

**最后更新**: 2025-12-11
**版本**: 1.0.0
