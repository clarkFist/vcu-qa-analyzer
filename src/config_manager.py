#!/usr/bin/env python3
"""
配置管理器
=========

管理用户配置和偏好设置
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器"""

    DEFAULT_CONFIG = {
        'theme': 'default',
        'embed_images': True,
        'process_mermaid': True,
        'output_dir': None,
        'batch_settings': {
            'recursive': True,
            'pattern': '*.md',
            'max_workers': 4
        },
        'advanced': {
            'minify_html': False,
            'add_toc': True,
            'add_footer': True,
            'custom_css': None
        }
    }

    def __init__(self, config_dir: Optional[Path] = None):
        """
        初始化配置管理器

        Args:
            config_dir: 配置目录（默认为用户主目录下的.md2html）
        """
        if config_dir is None:
            self.config_dir = Path.home() / '.md2html'
        else:
            self.config_dir = Path(config_dir)

        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / 'config.json'
        self.presets_dir = self.config_dir / 'presets'
        self.presets_dir.mkdir(exist_ok=True)

        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        加载配置文件

        Returns:
            配置字典
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置（处理新增配置项）
                    return self._merge_configs(self.DEFAULT_CONFIG, config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ 配置文件读取失败，使用默认配置: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # 创建默认配置文件
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()

    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        保存配置文件

        Args:
            config: 配置字典（默认使用当前配置）

        Returns:
            是否成功
        """
        if config is None:
            config = self.config

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"❌ 配置文件保存失败: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键（支持点分隔的嵌套键）
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        设置配置值

        Args:
            key: 配置键（支持点分隔的嵌套键）
            value: 配置值
        """
        keys = key.split('.')
        config = self.config

        # 导航到目标位置
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # 设置值
        config[keys[-1]] = value
        self.save_config()

    def update(self, updates: Dict[str, Any]) -> None:
        """
        批量更新配置

        Args:
            updates: 更新字典
        """
        self.config = self._merge_configs(self.config, updates)
        self.save_config()

    def reset(self) -> None:
        """重置为默认配置"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()

    def save_preset(self, name: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        保存配置预设

        Args:
            name: 预设名称
            config: 配置字典（默认使用当前配置）

        Returns:
            是否成功
        """
        if config is None:
            config = self.config

        preset_file = self.presets_dir / f"{name}.json"

        try:
            with open(preset_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"✅ 预设保存成功: {name}")
            return True
        except IOError as e:
            print(f"❌ 预设保存失败: {e}")
            return False

    def load_preset(self, name: str) -> Optional[Dict[str, Any]]:
        """
        加载配置预设

        Args:
            name: 预设名称

        Returns:
            配置字典或None
        """
        preset_file = self.presets_dir / f"{name}.json"

        if not preset_file.exists():
            print(f"⚠️ 预设不存在: {name}")
            return None

        try:
            with open(preset_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"✅ 预设加载成功: {name}")
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ 预设加载失败: {e}")
            return None

    def apply_preset(self, name: str) -> bool:
        """
        应用配置预设

        Args:
            name: 预设名称

        Returns:
            是否成功
        """
        preset = self.load_preset(name)
        if preset:
            self.config = preset
            self.save_config()
            return True
        return False

    def list_presets(self) -> list:
        """
        列出所有预设

        Returns:
            预设名称列表
        """
        presets = []
        for file in self.presets_dir.glob("*.json"):
            presets.append(file.stem)
        return sorted(presets)

    def delete_preset(self, name: str) -> bool:
        """
        删除预设

        Args:
            name: 预设名称

        Returns:
            是否成功
        """
        preset_file = self.presets_dir / f"{name}.json"

        if preset_file.exists():
            try:
                preset_file.unlink()
                print(f"✅ 预设删除成功: {name}")
                return True
            except IOError as e:
                print(f"❌ 预设删除失败: {e}")
                return False
        else:
            print(f"⚠️ 预设不存在: {name}")
            return False

    def export_config(self, path: Path) -> bool:
        """
        导出配置到文件

        Args:
            path: 导出路径

        Returns:
            是否成功
        """
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"✅ 配置导出成功: {path}")
            return True
        except IOError as e:
            print(f"❌ 配置导出失败: {e}")
            return False

    def import_config(self, path: Path) -> bool:
        """
        从文件导入配置

        Args:
            path: 导入路径

        Returns:
            是否成功
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.config = self._merge_configs(self.DEFAULT_CONFIG, config)
                self.save_config()
                print(f"✅ 配置导入成功: {path}")
                return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ 配置导入失败: {e}")
            return False

    def _merge_configs(self, base: dict, update: dict) -> dict:
        """
        合并配置字典

        Args:
            base: 基础配置
            update: 更新配置

        Returns:
            合并后的配置
        """
        result = base.copy()

        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def show_config(self) -> str:
        """
        显示当前配置

        Returns:
            格式化的配置字符串
        """
        return json.dumps(self.config, ensure_ascii=False, indent=2)

    def interactive_config(self):
        """交互式配置"""
        while True:
            print("\n" + "=" * 50)
            print("⚙️  配置管理器")
            print("=" * 50)
            print("1. 查看当前配置")
            print("2. 修改配置项")
            print("3. 保存为预设")
            print("4. 加载预设")
            print("5. 列出所有预设")
            print("6. 删除预设")
            print("7. 重置为默认")
            print("8. 导出配置")
            print("9. 导入配置")
            print("0. 退出")

            choice = input("\n请选择 [0-9]: ").strip()

            if choice == '1':
                print("\n当前配置:")
                print(self.show_config())

            elif choice == '2':
                self._interactive_modify()

            elif choice == '3':
                name = input("预设名称: ").strip()
                if name:
                    self.save_preset(name)

            elif choice == '4':
                presets = self.list_presets()
                if presets:
                    print("\n可用预设:")
                    for i, preset in enumerate(presets, 1):
                        print(f"  {i}. {preset}")
                    idx = input("\n选择预设编号: ").strip()
                    try:
                        preset_name = presets[int(idx) - 1]
                        self.apply_preset(preset_name)
                    except (ValueError, IndexError):
                        print("❌ 无效的选择")
                else:
                    print("⚠️ 没有可用的预设")

            elif choice == '5':
                presets = self.list_presets()
                if presets:
                    print("\n预设列表:")
                    for preset in presets:
                        print(f"  - {preset}")
                else:
                    print("⚠️ 没有预设")

            elif choice == '6':
                presets = self.list_presets()
                if presets:
                    print("\n预设列表:")
                    for i, preset in enumerate(presets, 1):
                        print(f"  {i}. {preset}")
                    idx = input("\n选择要删除的预设: ").strip()
                    try:
                        preset_name = presets[int(idx) - 1]
                        confirm = input(f"确认删除 '{preset_name}'? [y/N]: ").lower()
                        if confirm == 'y':
                            self.delete_preset(preset_name)
                    except (ValueError, IndexError):
                        print("❌ 无效的选择")
                else:
                    print("⚠️ 没有预设")

            elif choice == '7':
                confirm = input("确认重置为默认配置? [y/N]: ").lower()
                if confirm == 'y':
                    self.reset()
                    print("✅ 已重置为默认配置")

            elif choice == '8':
                path = input("导出路径 (如: config.json): ").strip()
                if path:
                    self.export_config(Path(path))

            elif choice == '9':
                path = input("导入路径: ").strip()
                if path and Path(path).exists():
                    self.import_config(Path(path))
                else:
                    print("❌ 文件不存在")

            elif choice == '0':
                break

            else:
                print("❌ 无效的选择")

    def _interactive_modify(self):
        """交互式修改配置"""
        print("\n常用配置项:")
        print("1. 默认主题")
        print("2. 图片嵌入")
        print("3. Mermaid处理")
        print("4. 批量转换设置")

        choice = input("\n选择要修改的项 [1-4]: ").strip()

        if choice == '1':
            themes = ['default', 'minimal', 'professional']
            print(f"\n当前主题: {self.get('theme')}")
            print("可用主题:")
            for i, theme in enumerate(themes, 1):
                print(f"  {i}. {theme}")
            idx = input("选择主题 [1-3]: ").strip()
            try:
                theme = themes[int(idx) - 1]
                self.set('theme', theme)
                print(f"✅ 主题已设置为: {theme}")
            except (ValueError, IndexError):
                print("❌ 无效的选择")

        elif choice == '2':
            current = self.get('embed_images')
            new_value = not current
            self.set('embed_images', new_value)
            print(f"✅ 图片嵌入: {'开启' if new_value else '关闭'}")

        elif choice == '3':
            current = self.get('process_mermaid')
            new_value = not current
            self.set('process_mermaid', new_value)
            print(f"✅ Mermaid处理: {'开启' if new_value else '关闭'}")

        elif choice == '4':
            print("\n批量转换设置:")
            print(f"1. 递归子目录: {self.get('batch_settings.recursive')}")
            print(f"2. 文件匹配模式: {self.get('batch_settings.pattern')}")
            print(f"3. 并发数: {self.get('batch_settings.max_workers')}")

            sub_choice = input("\n选择要修改的项 [1-3]: ").strip()

            if sub_choice == '1':
                current = self.get('batch_settings.recursive')
                self.set('batch_settings.recursive', not current)
                print(f"✅ 递归子目录: {'开启' if not current else '关闭'}")

            elif sub_choice == '2':
                pattern = input("文件匹配模式 (如 *.md): ").strip()
                if pattern:
                    self.set('batch_settings.pattern', pattern)
                    print(f"✅ 匹配模式: {pattern}")

            elif sub_choice == '3':
                workers = input("并发数 (1-10): ").strip()
                try:
                    workers = min(10, max(1, int(workers)))
                    self.set('batch_settings.max_workers', workers)
                    print(f"✅ 并发数: {workers}")
                except ValueError:
                    print("❌ 无效的数字")


if __name__ == '__main__':
    # 测试配置管理器
    config = ConfigManager()
    config.interactive_config()