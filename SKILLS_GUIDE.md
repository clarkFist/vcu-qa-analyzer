# AI Skills 使用指南

完整的 AI 驱动 Skills 系统使用指南。

## 🎯 什么是 AI Skills？

AI Skills 是智能分析模块，可以：
- **理解项目**: 自动分析项目结构、代码和依赖
- **回答问题**: 像与专家对话一样询问项目相关问题
- **提供洞察**: 识别架构模式、代码问题和改进机会

## 🚀 快速开始

### 最简单的方式：交互式问答

```bash
# 启动项目问答
python skills/project_qa.py /path/to/your/project

# 然后问任何问题
❓ 您的问题: 项目结构如何？
❓ 您的问题: 代码质量怎么样？
❓ 您的问题: 有哪些依赖？
❓ 您的问题: 有什么改进建议？
```

### 单个问题模式

```bash
# 快速获取答案
python skills/project_qa.py ~/projects/my-app -q "项目评分是多少？"
```

### 代码洞察分析

```bash
# 深度代码分析
python skills/code_insight.py ~/projects/my-app
```

## 📚 详细使用

### 1. 项目问答 Skill

#### 支持的问题类型

| 类型 | 关键词 | 示例问题 |
|------|--------|---------|
| **结构** | 结构、目录、文件 | "项目结构如何？"<br>"有哪些目录？"<br>"文件是如何组织的？" |
| **质量** | 质量、复杂度、风格 | "代码质量怎么样？"<br>"复杂度如何？"<br>"有什么质量问题？" |
| **依赖** | 依赖、包、库 | "有哪些依赖？"<br>"使用了什么包？"<br>"依赖版本如何管理？" |
| **评分** | 评分、分数、等级 | "项目评分是多少？"<br>"等级是什么？"<br>"得分如何？" |
| **文件** | 有哪些、包含、列出 | "有哪些 Python 文件？"<br>"包含什么文件？"<br>"列出所有 .js 文件" |
| **改进** | 改进、优化、建议 | "有什么改进建议？"<br>"如何优化？"<br>"需要改进什么？" |

#### 使用示例

```bash
# 交互式模式（推荐）
python skills/project_qa.py ~/projects/my-app

# 单个问题
python skills/project_qa.py ~/projects/my-app -q "项目结构如何？"

# JSON 输出（用于脚本）
python skills/project_qa.py ~/projects/my-app -q "代码质量怎么样？" --json
```

#### Python API

```python
from pathlib import Path
from skills.project_qa import ProjectQASkill

# 初始化
skill = ProjectQASkill(Path('/path/to/project'))

# 问问题
result = skill.ask("项目结构如何？")
print(result['answer'])

# 交互模式
skill.interactive_mode()
```

### 2. 代码洞察 Skill

#### 分析维度

1. **架构模式识别**
   - MVC (Model-View-Controller)
   - 分层架构 (Layered Architecture)
   - 微服务 (Microservices)

2. **代码异味检测**
   - 长方法 (Long Method)
   - 大类 (Large Class)
   - 参数过多 (Too Many Parameters)

3. **函数特征分析**
   - 递归函数
   - 生成器函数
   - 异步函数
   - 装饰器使用

4. **类层次分析**
   - 继承关系
   - 抽象类
   - 数据类 (Dataclass)

#### 使用示例

```bash
# 完整分析
python skills/code_insight.py ~/projects/my-app

# 特定类别
python skills/code_insight.py ~/projects/my-app -c architecture_patterns
python skills/code_insight.py ~/projects/my-app -c code_smells
python skills/code_insight.py ~/projects/my-app -c function_analysis

# JSON 输出
python skills/code_insight.py ~/projects/my-app --json
```

#### Python API

```python
from pathlib import Path
from skills.code_insight import CodeInsightSkill

# 初始化
skill = CodeInsightSkill(Path('/path/to/project'))

# 获取所有洞察
insights = skill.get_insights()

# 获取特定类别
patterns = skill.get_insights('architecture_patterns')
smells = skill.get_insights('code_smells')

# 格式化输出
print(skill.format_insights())
```

### 3. Skill 管理器

统一管理所有 Skills。

#### 使用示例

```bash
# 交互式模式
python skills/skill_manager.py ~/projects/my-app

# 列出所有 Skills
python skills/skill_manager.py ~/projects/my-app --list

# 执行特定 Skill
python skills/skill_manager.py ~/projects/my-app --skill qa --question "项目结构如何？"
python skills/skill_manager.py ~/projects/my-app --skill insight
```

#### Python API

```python
from pathlib import Path
from skills.skill_manager import SkillManager

# 初始化管理器
manager = SkillManager(Path('/path/to/project'))

# 列出 Skills
skills = manager.list_skills()
for skill in skills:
    print(f"{skill['id']}: {skill['name']}")

# 使用 Skill
result = manager.execute('qa', 'ask', question="项目评分是多少？")
print(result['answer'])

# 获取 Skill 实例
insight_skill = manager.get_skill('insight')
print(insight_skill.format_insights())
```

## 💡 实际应用场景

### 场景 1: 快速了解新项目

```bash
# 第一步：获取项目概览
python skills/project_qa.py ~/new-project -q "项目结构如何？"

# 第二步：了解代码质量
python skills/project_qa.py ~/new-project -q "代码质量怎么样？"

# 第三步：查看依赖
python skills/project_qa.py ~/new-project -q "有哪些依赖？"

# 第四步：深度分析
python skills/code_insight.py ~/new-project
```

### 场景 2: 代码审查

```bash
# 运行完整分析
python skills/code_insight.py ~/project-to-review > review_report.txt

# 检查特定问题
python skills/code_insight.py ~/project-to-review -c code_smells --json | \
    python -m json.tool | grep -A 5 "severity.*high"
```

### 场景 3: 项目对比

```python
from pathlib import Path
from skills.skill_manager import SkillManager

projects = [
    Path('~/projects/app-v1'),
    Path('~/projects/app-v2'),
]

for project in projects:
    manager = SkillManager(project)
    result = manager.execute('qa', 'ask', question="项目评分是多少？")

    print(f"\n{project.name}:")
    print(result['answer'])
```

### 场景 4: CI/CD 集成

```yaml
# .github/workflows/code-quality.yml
name: Code Quality Check

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

      - name: Check project score
        run: |
          SCORE=$(python skills/project_qa.py . -q "项目评分是多少？" | grep -oE '[0-9]+' | head -1)
          echo "Project score: $SCORE/100"
          if [ "$SCORE" -lt 60 ]; then
            echo "::error::Project quality score is too low"
            exit 1
          fi

      - name: Detect code smells
        run: |
          python skills/code_insight.py . --json > insights.json
          SMELLS=$(python -c "import json; print(len(json.load(open('insights.json'))['code_smells']))")
          echo "Code smells detected: $SMELLS"
          if [ "$SMELLS" -gt 20 ]; then
            echo "::warning::Too many code smells detected"
          fi
```

### 场景 5: 定期报告

```bash
#!/bin/bash
# weekly_report.sh

DATE=$(date +%Y%m%d)
PROJECT_PATH="$1"
OUTPUT_DIR="reports"

mkdir -p "$OUTPUT_DIR"

echo "生成项目分析报告: $DATE"

# 项目概览
python skills/project_qa.py "$PROJECT_PATH" -q "项目结构如何？" > "$OUTPUT_DIR/overview_$DATE.txt"

# 质量评估
python skills/project_qa.py "$PROJECT_PATH" -q "代码质量怎么样？" >> "$OUTPUT_DIR/overview_$DATE.txt"

# 评分
python skills/project_qa.py "$PROJECT_PATH" -q "项目评分是多少？" >> "$OUTPUT_DIR/overview_$DATE.txt"

# 改进建议
python skills/project_qa.py "$PROJECT_PATH" -q "有什么改进建议？" >> "$OUTPUT_DIR/overview_$DATE.txt"

# 深度分析
python skills/code_insight.py "$PROJECT_PATH" > "$OUTPUT_DIR/insights_$DATE.txt"

echo "报告已生成: $OUTPUT_DIR/"
```

## 🔧 高级用法

### 1. 批量项目分析

```python
#!/usr/bin/env python3
"""批量分析多个项目"""

from pathlib import Path
from skills.skill_manager import SkillManager
import json

def analyze_projects(project_dirs):
    results = []

    for project_path in project_dirs:
        project_path = Path(project_path).expanduser()

        if not project_path.exists():
            continue

        print(f"\n分析: {project_path.name}")
        print("=" * 60)

        manager = SkillManager(project_path)

        # 获取评分
        score_result = manager.execute('qa', 'ask', question="项目评分是多少？")

        # 获取洞察
        insight_skill = manager.get_skill('insight')
        insights = insight_skill.get_insights()

        results.append({
            'project': project_path.name,
            'path': str(project_path),
            'score': score_result,
            'code_smells': len(insights['code_smells']),
            'architecture': insights['architecture_patterns']['detected_patterns']
        })

    # 保存结果
    with open('batch_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n结果已保存到: batch_analysis.json")

if __name__ == '__main__':
    projects = [
        '~/projects/app1',
        '~/projects/app2',
        '~/projects/app3',
    ]

    analyze_projects(projects)
```

### 2. 自定义问题处理

```python
from skills.project_qa import ProjectQASkill
from pathlib import Path

class CustomQASkill(ProjectQASkill):
    """自定义问答 Skill"""

    def _classify_question(self, question: str) -> str:
        """扩展问题分类"""
        # 添加自定义类别
        if '安全' in question or 'security' in question.lower():
            return 'security'

        # 调用父类方法
        return super()._classify_question(question)

    def _answer_security_question(self, question: str):
        """回答安全相关问题"""
        # 自定义安全分析逻辑
        return {
            'question': question,
            'type': 'security',
            'answer': '安全分析结果...',
            'details': {}
        }

# 使用自定义 Skill
skill = CustomQASkill(Path('/path/to/project'))
result = skill.ask("项目有哪些安全问题？")
print(result['answer'])
```

### 3. 集成外部工具

```python
from skills.code_insight import CodeInsightSkill
from pathlib import Path
import subprocess
import json

class EnhancedInsightSkill(CodeInsightSkill):
    """增强的洞察 Skill"""

    def _analyze_code(self):
        """扩展分析"""
        # 调用父类分析
        super()._analyze_code()

        # 添加 pylint 分析
        self.insights['pylint_results'] = self._run_pylint()

    def _run_pylint(self):
        """运行 pylint"""
        python_files = list(self.project_path.rglob("*.py"))[:5]
        results = []

        for file_path in python_files:
            try:
                result = subprocess.run(
                    ['pylint', str(file_path), '--output-format=json'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.stdout:
                    data = json.loads(result.stdout)
                    results.append({
                        'file': str(file_path.relative_to(self.project_path)),
                        'issues': len(data)
                    })
            except:
                pass

        return results

# 使用增强 Skill
skill = EnhancedInsightSkill(Path('/path/to/project'))
insights = skill.get_insights()
print(f"Pylint 结果: {insights['pylint_results']}")
```

## 📊 输出格式

### 文本格式

适合人类阅读：

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
```

### JSON 格式

适合程序处理：

```json
{
  "question": "项目结构如何？",
  "type": "structure",
  "answer": "...",
  "details": {
    "total_files": 45,
    "file_types": {
      "py": 30,
      "md": 5
    }
  }
}
```

## 🐛 故障排除

### 问题 1: 导入错误

```
ModuleNotFoundError: No module named 'src'
```

**解决方案**: 从项目根目录运行

```bash
cd /path/to/error_report
python skills/project_qa.py /path/to/target/project
```

### 问题 2: 分析速度慢

**解决方案**: 限制分析文件数量

编辑 Skill 文件，修改：
```python
for file_path in python_files[:10]:  # 只分析前 10 个
```

### 问题 3: 内存占用高

**解决方案**: 使用生成器

```python
def _scan_files_generator(self):
    for file_path in self.project_path.rglob("*.py"):
        yield file_path
```

## 📚 相关文档

- [Skills README](skills/README.md) - 详细技术文档
- [项目分析模块](src/analyzers/README.md) - 底层分析引擎
- [使用示例](USAGE_EXAMPLES.md) - 更多示例

## 🎓 最佳实践

1. **先问概览问题**: 从"项目结构如何？"开始
2. **逐步深入**: 根据答案提出更具体的问题
3. **结合使用**: 问答 + 洞察分析获得完整视图
4. **定期分析**: 设置定时任务跟踪项目健康度
5. **集成 CI/CD**: 自动化质量检查

---

**最后更新**: 2025-12-11
**版本**: 1.0.0
