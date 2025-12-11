#!/usr/bin/env python3
"""
Mermaid 图表处理器
=================

处理 Markdown 中的 Mermaid 图表代码块
"""

import re


class MermaidProcessor:
    """Mermaid 图表处理器"""

    def __init__(self):
        """初始化处理器"""
        # Mermaid 代码块模式
        self.pattern = r'```mermaid\n(.*?)\n```'

    def process(self, content: str) -> str:
        """
        处理 Markdown 中的 Mermaid 代码块

        Args:
            content: Markdown 内容

        Returns:
            处理后的内容
        """
        def replace_mermaid(match):
            mermaid_code = match.group(1)
            # 转换为可被 Mermaid.js 识别的 div 元素
            return f'<div class="mermaid">\n{mermaid_code}\n</div>'

        # 替换所有 Mermaid 代码块
        processed = re.sub(self.pattern, replace_mermaid, content, flags=re.DOTALL)

        return processed

    def extract_diagrams(self, content: str) -> list[str]:
        """
        提取所有 Mermaid 图表代码

        Args:
            content: Markdown 内容

        Returns:
            Mermaid 代码列表
        """
        matches = re.findall(self.pattern, content, flags=re.DOTALL)
        return matches

    def has_mermaid(self, content: str) -> bool:
        """
        检查是否包含 Mermaid 图表

        Args:
            content: Markdown 内容

        Returns:
            是否包含 Mermaid
        """
        return bool(re.search(self.pattern, content, flags=re.DOTALL))

    def get_mermaid_script(self) -> str:
        """
        获取 Mermaid.js 加载脚本

        Returns:
            JavaScript 代码
        """
        return '''
        // Mermaid.js 多CDN加载策略
        (function() {
            const cdns = [
                'https://cdn.bootcdn.net/ajax/libs/mermaid/10.6.1/mermaid.min.js',
                'https://unpkg.com/mermaid@10/dist/mermaid.min.js',
                'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'
            ];

            let loaded = false;
            let currentIndex = 0;

            function loadScript(url, onSuccess, onError) {
                const script = document.createElement('script');
                script.src = url;
                script.onload = onSuccess;
                script.onerror = onError;
                script.async = false;
                document.head.appendChild(script);
            }

            function tryNextCDN() {
                if (currentIndex >= cdns.length) {
                    console.error('所有Mermaid CDN加载失败');
                    window.mermaidLoadFailed = true;
                    handleMermaidFallback();
                    return;
                }

                loadScript(
                    cdns[currentIndex],
                    function() {
                        loaded = true;
                        console.log('Mermaid已从CDN加载:', cdns[currentIndex]);
                        initMermaid();
                    },
                    function() {
                        currentIndex++;
                        tryNextCDN();
                    }
                );
            }

            function initMermaid() {
                if (typeof mermaid !== 'undefined') {
                    try {
                        mermaid.initialize({
                            startOnLoad: true,
                            theme: 'default',
                            securityLevel: 'loose',
                            flowchart: {
                                useMaxWidth: true,
                                htmlLabels: true,
                                curve: 'basis'
                            }
                        });
                        console.log('Mermaid初始化成功');
                    } catch (e) {
                        console.error('Mermaid初始化失败:', e);
                        handleMermaidFallback();
                    }
                }
            }

            function handleMermaidFallback() {
                // 降级显示：将 Mermaid 转换为文本
                document.querySelectorAll('.mermaid').forEach(function(element) {
                    if (!element.classList.contains('mermaid-fallback')) {
                        const text = element.textContent.trim();
                        element.classList.add('mermaid-fallback');
                        element.innerHTML = '<pre>' + text + '</pre>';
                    }
                });
            }

            // 开始加载
            tryNextCDN();
        })();
        '''