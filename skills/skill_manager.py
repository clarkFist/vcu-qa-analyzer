#!/usr/bin/env python3
"""
AI Skills 管理器

统一管理和调用所有 AI 驱动的 Skills
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.project_qa import ProjectQASkill
from skills.code_insight import CodeInsightSkill


class SkillManager:
    """Skills 管理器"""

    def __init__(self, project_path: Path):
        """
        初始化管理器

        Args:
            project_path: 项目路径
        """
        self.project_path = Path(project_path)
        self.skills = {}
        self._register_skills()

    def _register_skills(self):
        """注册所有可用的 Skills"""
        self.skills = {
            'qa': {
                'name': '项目问答',
                'description': '回答关于项目的问题',
                'class': ProjectQASkill,
                'instance': None
            },
            'insight': {
                'name': '代码洞察',
                'description': '深度代码分析和架构洞察',
                'class': CodeInsightSkill,
                'instance': None
            }
        }

    def list_skills(self) -> List[Dict[str, str]]:
        """列出所有可用的 Skills"""
        return [
            {
                'id': skill_id,
                'name': info['name'],
                'description': info['description']
            }
            for skill_id, info in self.skills.items()
        ]

    def get_skill(self, skill_id: str):
        """
        获取 Skill 实例

        Args:
            skill_id: Skill ID

        Returns:
            Skill 实例
        """
        if skill_id not in self.skills:
            raise ValueError(f"未知的 Skill: {skill_id}")

        skill_info = self.skills[skill_id]

        # 懒加载
        if skill_info['instance'] is None:
            print(f"🔧 正在加载 Skill: {skill_info['name']}...")
            skill_info['instance'] = skill_info['class'](self.project_path)

        return skill_info['instance']

    def execute(self, skill_id: str, action: str, **kwargs) -> Any:
        """
        执行 Skill 操作

        Args:
            skill_id: Skill ID
            action: 操作名称
            **kwargs: 操作参数

        Returns:
            操作结果
        """
        skill = self.get_skill(skill_id)

        if not hasattr(skill, action):
            raise ValueError(f"Skill '{skill_id}' 没有操作 '{action}'")

        method = getattr(skill, action)
        return method(**kwargs)

    def interactive_mode(self):
        """交互式模式"""
        print(f"\n{'='*60}")
        print(f"🤖 AI Skills 管理器")
        print(f"{'='*60}")
        print(f"项目: {self.project_path.name}")
        print(f"路径: {self.project_path}")
        print(f"{'='*60}\n")

        print("可用的 Skills:\n")
        for skill_info in self.list_skills():
            print(f"  [{skill_info['id']}] {skill_info['name']}")
            print(f"      {skill_info['description']}\n")

        print("💡 提示: 输入 'quit' 或 'exit' 退出\n")

        while True:
            try:
                # 选择 Skill
                skill_id = input("🎯 选择 Skill (qa/insight): ").strip().lower()

                if not skill_id:
                    continue

                if skill_id in ['quit', 'exit', 'q']:
                    print("\n👋 再见！")
                    break

                if skill_id not in self.skills:
                    print(f"❌ 未知的 Skill: {skill_id}\n")
                    continue

                # 根据 Skill 类型执行不同操作
                if skill_id == 'qa':
                    question = input("❓ 您的问题: ").strip()
                    if question:
                        result = self.execute('qa', 'ask', question=question)
                        print(f"\n💬 回答:\n")
                        print(result['answer'])
                        print(f"\n{'-'*60}\n")

                elif skill_id == 'insight':
                    skill = self.get_skill('insight')
                    print("\n" + skill.format_insights())
                    print(f"\n{'-'*60}\n")

            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 错误: {str(e)}\n")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='AI Skills 管理器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式模式
  python skill_manager.py /path/to/project

  # 列出所有 Skills
  python skill_manager.py /path/to/project --list

  # 执行特定 Skill
  python skill_manager.py /path/to/project --skill qa --action ask --question "项目结构如何？"

  # JSON 输出
  python skill_manager.py /path/to/project --skill insight --json
        """
    )

    parser.add_argument(
        'project_path',
        help='项目路径'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='列出所有可用的 Skills'
    )

    parser.add_argument(
        '--skill',
        choices=['qa', 'insight'],
        help='要使用的 Skill'
    )

    parser.add_argument(
        '--action',
        help='要执行的操作'
    )

    parser.add_argument(
        '--question',
        help='问题（用于 qa skill）'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='以 JSON 格式输出'
    )

    args = parser.parse_args()

    # 验证项目路径
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"❌ 错误: 项目路径不存在: {project_path}")
        return 1

    # 初始化管理器
    manager = SkillManager(project_path)

    # 列出 Skills
    if args.list:
        skills = manager.list_skills()
        if args.json:
            print(json.dumps(skills, indent=2, ensure_ascii=False))
        else:
            print("\n可用的 Skills:\n")
            for skill in skills:
                print(f"  [{skill['id']}] {skill['name']}")
                print(f"      {skill['description']}\n")
        return 0

    # 执行特定 Skill
    if args.skill:
        if args.skill == 'qa':
            if not args.question:
                print("❌ 错误: qa skill 需要 --question 参数")
                return 1

            result = manager.execute('qa', 'ask', question=args.question)

            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"\n❓ 问题: {result['question']}\n")
                print(f"💬 回答:\n")
                print(result['answer'])

        elif args.skill == 'insight':
            skill = manager.get_skill('insight')

            if args.json:
                insights = skill.get_insights()
                print(json.dumps(insights, indent=2, ensure_ascii=False))
            else:
                print(skill.format_insights())

        return 0

    # 交互式模式
    manager.interactive_mode()

    return 0


if __name__ == '__main__':
    sys.exit(main())
